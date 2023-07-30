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
        output_data = None
        for page in meta_data:            
            page_url = page['url']
            print(f'opening page {page_url}')
            driver.get(page_url)

            container_data = get_container_data(driver, config)

            if config['mutateMetadata']:
                for data in container_data:
                    for key in list(data.keys()):                    
                        page[key] = data[key]
        
        if config['mutateMetadata']:
            output_data = meta_data
        else:
            output_data = container_data
        return output_data


    except (TimeoutException) as ex:
        print(f'TimeoutException happened')
        pass
    finally:
        pass
        driver.quit()


def get_location_constant(container_locate_by):
    if container_locate_by == 'CSS_SELECTOR':
        container_locate_by_ec = By.CSS_SELECTOR
    elif container_locate_by == 'CLASS_NAME':
        container_locate_by_ec = By.CLASS_NAME
    else:
        pass
        print(f'Unsupported locator container_locate_by {container_locate_by}')
        # probably needs to throw something...
    return container_locate_by_ec


def get_element(driver, content_config, condition, locate_by_ec, locate_by_value, index):    
    err, items = return_elements(driver, content_config, condition, locate_by_ec, locate_by_value)
    if err:
        return err, None
    return err, items[index]


def get_elements(driver, content_config, condition, locate_by_ec, locate_by_value):
    return return_elements(driver, content_config, condition, locate_by_ec, locate_by_value)


def return_elements(driver, content_config, condition, locate_by_ec, locate_by_value):
    try:
        timeout = content_config['timeout']
        WebDriverWait(driver, timeout).until(condition)
        container_element = driver.find_elements(locate_by_ec, locate_by_value)        
        return False, container_element
    except (TimeoutException) as ex:
        print(f'TimeoutException happened, element not found within {timeout} seconds')
        return True, None
    finally:
        pass
          

def get_container_data(driver, config):
    container_data = []
    for index, content_config in enumerate(config['contentContainers']):
        print(f'attempting to find the container with index {index}')
        container_locate_by = content_config['locateBy']
        container_locate_by_value = content_config['locateByValue']
        container_locate_by_ec = get_location_constant(container_locate_by)
        container_is_present = EC.presence_of_element_located((container_locate_by_ec, container_locate_by_value))
        container_index = content_config['index']
        error, container_element = get_element(driver, content_config, container_is_present, container_locate_by_ec, container_locate_by_value, container_index)
        if error:
            print(f'attempting to find the next container')        
            continue
        content_item_locate_by = content_config['contentItem']['locateBy']
        content_item_locate_by_value = content_config['contentItem']['locateByValue']
        content_item_locate_by_ec = get_location_constant(content_item_locate_by)
        content_item_is_present = EC.presence_of_element_located((content_item_locate_by_ec, content_item_locate_by_value))
        if content_config['contentItem']['type'] == 'firstItem':
            err, item = get_element(container_element, content_config, content_item_is_present, content_item_locate_by_ec, content_item_locate_by_value, 0)
            item_data = get_item_data(content_config, item)
            container_data.append(item_data)
        elif content_config['contentItem']['type'] == 'listUniqKeys':
            err, items = get_elements(container_element, content_config, content_item_is_present, content_item_locate_by_ec, content_item_locate_by_value)            
            for item in items:
                item_data = get_item_data(content_config, item)
                container_data.append(item_data)                
        elif content_config['contentItem']['type'] == 'list':
            err, items = get_elements(container_element, content_config, content_item_is_present, content_item_locate_by_ec, content_item_locate_by_value)            
            for item in items:
                item_data = get_item_data(content_config, item)
                for value in item_data.values():
                    pair = value.split(':')
                    container_data.append({pair[0]: pair[1].strip()})
                #print(f'item_data {item_data}')

    return container_data    


def get_item_data(content_config, item):
    new_item = {}    
    for selectValue in content_config['contentItem']['selectValues']:
        if selectValue['selectTarget'] == 'attribute':
            attribute = selectValue['selectValue']
            value = item.get_attribute(attribute)
            new_item[selectValue['keyName']] = value
        elif selectValue['selectTarget'] == 'text':                            
            value = item.text
            new_item[selectValue['keyName']] = value
    return new_item

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