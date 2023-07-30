from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from urllib.parse import urljoin

def scrape(meta_data, config):
    try:
        timeout, driver = setup_driver()

        container_locate_by = config['contentContainer']['locateBy']
        container_locate_by_value = config['contentContainer']['locateByValue']

        scraped_data = []
        output_data = None

        if container_locate_by == 'CSS_SELECTOR':
            container_locate_by_ec = By.CSS_SELECTOR
        elif container_locate_by == 'CLASS_NAME':
            container_locate_by_ec = By.CLASS_NAME
        else:
            print(f'Unsupported locator container_locate_by {container_locate_by}')
            exit()

        items_locate_by = config['contentItem']['locateBy']
        items_locate_by_value = config['contentItem']['locateByValue']

        if items_locate_by == 'CSS_SELECTOR':
            items_locate_by_ec = By.CSS_SELECTOR
        elif items_locate_by == 'CLASS_NAME':
            items_locate_by_ec = By.CLASS_NAME
        else:
            print(f'Unsupported locator items_locate_by {items_locate_by}')
            exit()
        
        container_is_present = EC.presence_of_element_located((container_locate_by_ec, container_locate_by_value))
        item_is_present = EC.presence_of_element_located((items_locate_by_ec, items_locate_by_value))

        for page in meta_data:
            page_url = page['url']
            print(f'opening page {page_url}')
            driver.get(page_url)
            WebDriverWait(driver, timeout).until(container_is_present)
            container = driver.find_elements(container_locate_by_ec, container_locate_by_value)
            if len(container) == 1:
                WebDriverWait(driver, timeout).until(item_is_present)
                items = container[0].find_elements(items_locate_by_ec, items_locate_by_value)
                print(f'item count is {len(items)}')
                for item in items:
                    new_item = {}                    
                    for selectValue in config['contentItem']['selectValues']:
                        if selectValue['selectTarget'] == 'attribute':
                            attribute = selectValue['selectValue']
                            value = item.get_attribute(attribute)
                            new_item[selectValue['keyName']] = value
                            scraped_data.append(new_item)
                        elif selectValue['selectTarget'] == 'text':                            
                            value = item.text
                            new_item[selectValue['keyName']] = value
                            scraped_data.append(new_item)
                    
                if config['mutateMetadata']:
                    page['items'] = scraped_data
            else:
                print(f'container count is not 1')
                exit()
        
        if config['mutateMetadata']:
            output_data = meta_data
        else:
            output_data = scraped_data
        
        driver.quit()
        return output_data


    except (TimeoutException) as ex:
        pass
    finally:
        pass
        driver.quit()

def setup_driver():
    driver_service = Service('.\chromedriver_win32\chromedriver.exe')
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--incognito')
    option.add_argument('--disable-dev-sh-usage')
    timeout = 15
    driver = webdriver.Chrome(service=driver_service, options=option)
    return timeout,driver