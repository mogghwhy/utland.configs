import csv
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from urllib.parse import urljoin

base_url = 'https://tv.nrk.no'
utland_url = 'programmer/utland'
url = urljoin(base_url, utland_url)

content_items_list = []

try:
    start = time.time()
    driver_service = Service('.\chromedriver_win32\chromedriver.exe')
    option = webdriver.ChromeOptions()
    #option.add_argument('--headless')
    option.add_argument('--no-sandbox')
    option.add_argument('--incognito')
    option.add_argument('--disable-dev-sh-usage')
    timeout = 15
    fieldnames = ['']
    driver = webdriver.Chrome(service=driver_service, options=option)
    

    content_list_container_cn = 'tv-cl-contentList'
    content_list_tag_name = 'li'
    content_item_tag_name = 'a'    
    content_tag_item_cn = 'tv-cl-letter-elements__list-element'
    content_tag_item_info_cn = 'tv-cl-letter-element'

    ps_container_id = 'app-main'
    episode_details_container_cn = 'tv-series-season-grid__episode-details'
    episode_description_cn = 'p.tv-series-episode-metadata__episode-description'
    
    content_list_container_present = EC.presence_of_element_located((By.CLASS_NAME,content_list_container_cn))
    content_tag_item_present = EC.presence_of_element_located((By.CLASS_NAME,content_tag_item_cn))
    episode_details_container_present = EC.presence_of_element_located((By.ID,ps_container_id))

    driver.get(url)
    WebDriverWait(driver, timeout).until(content_list_container_present)

    # expecting that there is a single item with this class name
    content_list_container = driver.find_element(By.CLASS_NAME,content_list_container_cn)

    content_list_elements = content_list_container.find_elements(By.TAG_NAME, content_list_tag_name)    

    # collect meta data about each alphabet letter
    for content_item in content_list_elements:
        content_item_tag = content_item.find_element(By.TAG_NAME, content_item_tag_name)
        item = {}
        href = content_item_tag.get_attribute('href')
        letter_id = content_item_tag.get_attribute('data-letter-id')
        print(f'getting data for {letter_id}')
        item['url'] = urljoin(base_url, href)
        item['letter_id'] = letter_id
        content_items_list.append(item)

    # collect meta data about each movie in alphabet letter
    #for content_item in content_items_list[2:3]:
    for content_item in content_items_list:
        driver.get(content_item['url'])        
        WebDriverWait(driver, timeout).until(content_tag_item_present)
        content_tag_items = driver.find_elements(By.CLASS_NAME, content_tag_item_cn)
        count = len(content_tag_items)
        print(f'count of items in {content_item["letter_id"]} {count}')
        content_item['count'] = count
        media = []
        for content_tag_item in content_tag_items:
            content_tag_item_info = content_tag_item.find_element(By.CLASS_NAME, content_tag_item_info_cn)
            href = content_tag_item_info.get_attribute('href')            
            title = content_tag_item_info.text
            media.append({'url':urljoin(base_url, href),'title':title})

        content_item['media'] = media
            
    
    # collect info about each movie in alphabet letter
    #for content_item in content_items_list[2:3]:
    for content_item in content_items_list:
        medias = content_item['media']

        #for media in medias[:4]:
        for media in medias:
            series = True
            media_url = media['url']
            print(f'opening {media_url}')
            driver.get(media_url)
            WebDriverWait(driver, timeout).until(episode_details_container_present)
            episode_details_container = None
            sections = None
            description = None

            episode_details_container = driver.find_elements(By.CSS_SELECTOR, 'main.tv-series')
            if len(episode_details_container) == 0:
                episode_details_container = driver.find_elements(By.CSS_SELECTOR, 'main.tv-program')
                series = False

            if series:
                episode_description = episode_details_container[0].find_elements(By.CSS_SELECTOR, episode_description_cn)
                sections = episode_details_container[0].find_elements(By.CSS_SELECTOR, 'section.tv-series-section')
            else:
                episode_description = episode_details_container[0].find_elements(By.CSS_SELECTOR, 'div.tv-program-description')
                sections = episode_details_container[0].find_elements(By.CSS_SELECTOR, 'section.tv-program-section')
            
            if len(episode_description) > 0:
                description = episode_description[0].text
            section = sections[1]
            infos = episode_details_container[0].find_elements(By.CSS_SELECTOR, 'li.tv-series-more-info-item')            

            media['description'] = description

            for info in infos:                
                key = info.find_elements(By.CSS_SELECTOR, 'span.tv-series-more-info-item__title')[0].text.split(":")[0]
                value = info.find_elements(By.CSS_SELECTOR, 'span.tv-series-more-info-item__value')[0].text
                print(f'{key}, {value}')
                media[key] = value
        
    #print(f'cc {content_items_list[2:3]}')
    json_data = json.dumps(content_items_list)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    
    
except (TimeoutException) as py_ex:
    pass
finally:
    pass
    end = time.time()
    print("The time of execution:", end-start)
    print("finally block")
    driver.quit()
