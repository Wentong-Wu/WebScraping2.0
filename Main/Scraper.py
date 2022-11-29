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

if __name__ == "__main__":
    website = Scraper("https://www.waterstones.com/")
    website.accept_cookies()
    nav_name = ["NEW","COMING SOON","SPECIAL EDITIONS"]
    website.get_navigation_bar(nav_name[1])
    pass
