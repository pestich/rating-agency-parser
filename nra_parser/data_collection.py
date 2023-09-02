import time
import pandas as pd
import urllib.request
from tqdm import tqdm
tqdm.pandas()
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_text_general(web_element) -> str:
    soup = BeautifulSoup(web_element.get_attribute('outerHTML'), "html.parser")
    paragraphs = soup.find_all('p')
    result = ''
    for paragraph in paragraphs:
        result += (paragraph.text.strip() + '\n')
    return result


def get_text_add(web_element) -> str:
    soup = BeautifulSoup(web_element.get_attribute('outerHTML'), "html.parser")
    paragraphs = soup.find_all('p')
    blocks = soup.find_all('ul')
    result = ''
    for i in range(len(paragraphs)):
        result += (paragraphs[i].text.strip() + '\n')
        try: 
            lines = blocks[i].find_all('li')
            for line in lines:
                result += (line.text.strip() + '\n')
        except:
            continue
    return result


def parse_text(link: str) -> str:
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        browser = webdriver.Chrome(options=options)
        browser.get(link)
        time.sleep(2)

        browser.find_element(By.XPATH, '/html/body/div[2]/div/section[2]/div/div[2]/div/div/div/div/section/div/nav/ul/li[1]/a/span').click()
        text = browser.find_element(By.XPATH, '/html/body/div[2]/div/section[2]/div/div[2]/div/div/div/div/section/div/div/section[1]/div/div/span')
        part_1 = get_text_general(text)
        time.sleep(1)

        browser.find_element(By.XPATH, '/html/body/div[2]/div/section[2]/div/div[2]/div/div/div/div/section/div/nav/ul/li[2]/a/span').click()
        text = browser.find_element(By.XPATH, '/html/body/div[2]/div/section[2]/div/div[2]/div/div/div/div/section/div/div/section[2]/div/div/span')
        part_2 = get_text_add(text)
        time.sleep(1)

        browser.quit()

        return part_1 + part_2
    except:
        return None
    

destination = 'nra_data.xlsx'
url = 'https://www.ra-national.ru/wp-load.php?security_key=100c906f36a0b90e&export_id=20&action=get_data'
urllib.request.urlretrieve(url, destination)

df = pd.read_excel('nra_data.xlsx')

df['text'] = df['Ссылка на пресс релиз'].progress_apply(parse_text)

df.to_csv('../data_output/nra_all.csv')