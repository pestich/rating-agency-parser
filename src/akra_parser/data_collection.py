import time
import pandas as pd
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from math import ceil


BASE_URL = 'https://www.acra-ratings.ru'


def collect_data(web_element) -> None:
    soup = BeautifulSoup(web_element.get_attribute('outerHTML'), "html.parser")
    for row in soup.find_all(class_ = 'emits-row search-table-row'):
        temp = dict()
        columns = row.find_all(class_ ='emits-row__item')
        links = row.find_all('a')
        temp['name'] = columns[0].text.strip()
        temp['name_link'] = BASE_URL + links[0].get('href')
        temp['rating'] = columns[1].text.strip()
        temp['sector'] = columns[2].text.strip()
        temp['date'] = columns[3].text.strip()
        temp['press_release_link'] = BASE_URL + links[1].get('href')
        global data
        data.append(temp)


def get_text(web_element, idx) -> None:
    soup = BeautifulSoup(web_element.get_attribute('outerHTML'), "html.parser")
    paragraphs = soup.find_all('p')
    result = ''
    for paragraph in paragraphs:
        result += (paragraph.text.strip() + '\n')
    global data
    data[idx]['press_release_text'] = result


data = list()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.acra-ratings.ru/ratings/issuers/?text=&sectors[]=&activities[]=&countries[]=&forecasts[]\
        =&on_revision=0&rating_scale=106&rate_from=1&rate_to=23&page=1&sort=&count=10&')
time.sleep(2)

pages_quantity = browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div[1]')
pages_quantity = ceil(int(pages_quantity.text.split()[-1]) / 10)

for page in tqdm(range(1, pages_quantity+1)):
    browser.get(f'https://www.acra-ratings.ru/ratings/issuers/?text=&sectors[]=&activities[]=&countries[]=&forecasts[]\
        =&on_revision=0&rating_scale=106&rate_from=1&rate_to=23&page={page}&sort=&count=10&')
    time.sleep(3)
    table = browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/div/div[3]/div/div[2]/div[1]/div[1]/div/div')
    collect_data(table)

for i in tqdm(range(len(data))):
    browser.get(data[i]['press_release_link'])
    time.sleep(1)
    text = browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/div/div[1]/div[2]/div')
    get_text(text, i)

browser.quit()

data_json = json.dumps(data, indent = 4)
df = pd.read_json(data_json)
df.to_csv('akra_all.csv')