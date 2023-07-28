from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from urllib.parse import urljoin

def scrape(metadata, config):
    try:
        driver_service = Service('.\chromedriver_win32\chromedriver.exe')
        option = webdriver.ChromeOptions()
        #option.add_argument('--headless')
        option.add_argument('--no-sandbox')
        option.add_argument('--incognito')
        option.add_argument('--disable-dev-sh-usage')
        timeout = 15
        driver = webdriver.Chrome(service=driver_service, options=option)


    except (TimeoutException) as ex:
        pass
    finally:
        pass