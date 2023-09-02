import time
import pandas as pd
import json
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


BASE_URL = 'https://www.raexpert.ru'


def collect_data(web_element) -> None:
    soup = BeautifulSoup(web_element.get_attribute('outerHTML'), "html.parser")
    for row in soup.find_all('tr'):
        temp = dict()
        columns = row.find_all('td')
        links = row.find_all('a')
        temp['name'] = columns[0].text[:len(columns[0].text)//2].strip()
        temp['name_link'] = BASE_URL + links[0].get('href')
        temp['rating'] = columns[1].text
        temp['forecast'] = columns[2].text
        temp['date'] = columns[3].text
        temp['press_release_link'] = BASE_URL + links[1].get('href')
        global data
        data.append(temp)


def get_text(web_element, idx) -> None:
    soup = BeautifulSoup(web_element.get_attribute('outerHTML'), "html.parser")
    paragraphs = soup.find_all('p')
    result = ''
    for paragraph in paragraphs:
        result += (paragraph.text + '\n')
    global data
    data[idx]['press_release_text'] = result

data = list()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.raexpert.ru/ratings/bankcredit_all/')
time.sleep(1)
print('Starting...')
count = 1
while True:
    try:
        browser.find_element(By.XPATH, f'/html/body/main/div/div[2]/div/div[6]/span[{count}]').click()
        table = browser.find_element(By.XPATH, '/html/body/main/div/div[2]/div/div[5]/table/tbody')
        collect_data(table)
        time.sleep(1)
        if count < 7:
            count += 1
    except:
        break

for i in tqdm(range(len(data))):
    browser.get(data[i]['press_release_link'])
    time.sleep(1)
    text = browser.find_element(By.XPATH, '/html/body/main/div/div[2]/div[1]/div')
    get_text(text, i)

browser.quit()

data_json = json.dumps(data, indent = 4) 
df = pd.read_json(data_json)
df.to_csv('ra_banks.csv')

print('Parsing has finished')
