from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

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
        pass

if __name__ == "__main__":
    website = Scraper("https://www.waterstones.com/")
    website.accept_cookies()
    nav_name = ["NEW","COMING SOON","SPECIAL EDITIONS"]
    website.get_navigation_bar(nav_name[1])
    website.scroll_to_end()
    website.open_links(website.get_all_element_links())
    pass
