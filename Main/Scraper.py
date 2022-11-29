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

    def get_navigation_bar(self, class_name: str= 'navs'):
        nav_bar = self.driver.find_element(By.CLASS_NAME,class_name)
        nav_bar_list = nav_bar.find_elements(By.XPATH,'.//li')
        print(len(nav_bar_list))

if __name__ == "__main__":
    website = Scraper("https://www.waterstones.com/")
    website.accept_cookies()
    website.get_navigation_bar()
    pass
