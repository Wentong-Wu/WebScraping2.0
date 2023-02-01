from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import urllib.request
from pathlib import Path
import time
import os

class Scraper:

    def __init__(self, url) -> webdriver.Chrome():
        """
        Initializing the webpage
        """
        options = Options()
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        self.delay = 10

    def accept_cookies(self, xpath: str = '//*[@id="onetrust-accept-btn-handler"]'):
        #WebDriverWait = Explicit waits
        accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        time.sleep(1)
        accept_cookies_button.click()

    def get_navigation_bar(self, data_content):
        nav_bar = self.driver.find_element(By.XPATH, '//a[@data-content="'+data_content+'"]')
        nav_bar.click()

    def scroll_to_end(self):
        """
        Scrolls down to the end of the page.
        """
        #Scroll all the way down to get all the products
        length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
        page_end = False
        while(page_end==False):
            last_length_page = length_of_page
            time.sleep(1)
            length_of_page = self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight);var length_of_page=document.body.scrollHeight;return length_of_page;")
            if last_length_page==length_of_page:
                try:
                    self.driver.find_element(By.XPATH,'//*[@class="infinite-load"]').find_element(By.XPATH,'.//button').click()
                except:
                    page_end=True
                    
    def get_all_element_links(self, xpath: str = '//*[@class="search-results-list"]'):
        books = self.driver.find_element(By.XPATH,xpath)
        list_of_books = books.find_elements(By.XPATH,'.//*[@class="image-wrap"]/a')
        link_of_books = []
        for book in list_of_books:
            link_of_books.append(book.get_attribute("href"))
        return link_of_books
    
    def open_links(self, links):
        for link in links:
            self.driver.get(link)
            base = Path('raw_data')
            base.mkdir(exist_ok=True)
            with open(base/'data.json','w',encoding='utf-8') as f:
                json.dump(self.get_data,f,ensure_ascii=False,indent=4)
        
        # Download data into "raw_data"
        
            # //*[@itemprop="isbn"] - isbn
            # //*[@itemprop="price"] - price
            # //*[@itemprop="image"] - image
            # //*[@itemprop="numberOfPages"] - number of pages
            # //*[@itemprop="publisher"] - publisher
            # //*[@itemprop="name"] - title name
            # //*[@class="breadcrumbs span12"] - list of book genres
            # //*[@id="scope_book_author"] - book author
    
    def get_data(self) -> dict:
        single_data = {}
        single_data["Title"]=(self.driver.find_element(By.XPATH,'//*[@itemprop="name"]').text)
        try:
            single_data["Author"]=(self.driver.find_element(By.XPATH,'//*[@itemprop="author"]').text)
        except:
            single_data["Author"]=(self.driver.find_element(By.XPATH,'//*[@itemprop="name"]').text)
        single_data["Publisher"]=(self.driver.find_element(By.XPATH,'//*[@itemprop="publisher"]').get_attribute("textContent"))
        single_data["Price"]=(self.driver.find_element(By.XPATH,'//*[@itemprop="price"]').text)
        single_data["ISBN"]=(self.driver.find_element(By.XPATH,'//*[@itemprop="isbn"]').get_attribute("textContent"))
        single_data["Image"]=(self.driver.find_element(By.XPATH,'//*[@id="scope_book_image"]').get_attribute("src"))
        category_list = self.driver.find_elements(By.XPATH,'//*[@class="breadcrumbs span12"]/a')
        category = []
        for cate in category_list:
            category.append(cate.get_attribute("textContent"))
        single_data["Category"] = category

        

        # Download Image into "images" folder
        self.download_image(single_data.get("ISBN"),single_data.get("Image"))

        

        return single_data

    def download_image(self, uniqueID, prod_image):
        """
        Download image into a folder
        """
        #Save images into images folder

        base = Path('images')
        base.mkdir(exist_ok=True)
        opener = urllib.request.URLopener()
        opener.addheader("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        try:
            filename, headers = opener.retrieve(prod_image,os.path.join(base, ""+uniqueID+".jpg"))
        except:
            prod_image = "https://www.jamesgood.co.uk/sites/default/files/blog_images/waterstones-logo-square.png"
            filename, headers = opener.retrieve(prod_image,os.path.join(base, ""+uniqueID+".jpg"))
        

if __name__ == "__main__":
    website = Scraper("https://www.waterstones.com/")
    website.accept_cookies()
    nav_name = ["NEW","COMING SOON","SPECIAL EDITIONS"]
    website.get_navigation_bar(nav_name[1])
    website.scroll_to_end()

    website.open_links(website.get_all_element_links())
    pass
