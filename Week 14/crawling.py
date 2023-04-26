# crawling / scraping

# beautiful soup
# scrapy
# selenium

# -------------------

# 1- Speed
# 2- Ease of Use
# 3- Memory Usage
# 4- Dependency Requirements
# 5- Javascript Rendering


from selenium import webdriver
import sqlite3
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime

ch = webdriver.Chrome(ChromeDriverManager().install())

db = sqlite3.connect('housing')
cursor = db.cursor()

table_query = 'CREATE TABLE IF NOT EXISTS details ' \
              '(ad_id INTEGER, ' \
              'published_date TIMESTAMP, ' \
              'description TEXT, ' \
              'price REAL, ' \
              'location TEXT, ' \
              'area INTEGER ,' \
              'bedrooms INTEGER, ' \
              'url TEXT, ' \
              'agency TEXT, ' \
              'building_age INTEGER, ' \
              'building_type TEXT, ' \
              'PRIMARY KEY (ad_id))'  # TODO: challenge: write code to check for existing ids (bypass repetition)

cursor.execute(table_query)

# TODO: crawl all pages ---> change page index ---> &page=<variable>
url = "https://kilid.com/buy/tehran-satarkhan?listingTypeId=1&location=328363&sort=DATE_DESC&page=0"
ch.maximize_window()
ch.get(url)

time.sleep(2)

published_time = list()
description = list()
price = list()
location = list()
building_type = list()
area = list()
bedrooms = list()
urls = list()
ad_id = list()
agency = list()
building_age = list()  # TODO: challenge --> crawl each individual page

# ch.find_elements_by_xpath('//a[contain(@href, "detail")]')
info = ch.find_elements(By.XPATH, '//a[contains(@href, "detail")]')
for elem in info:
    temp = elem.text.split('\n')
    for t in temp:
        if 'قیمت هر متر مربع' in t:
            temp.remove(t)
    agency.append(temp[-1])
    published_time.append(temp[1])
    description.append(temp[2])
    price.append(temp[3].strip('قیمت:'))
    location.append(temp[4])
    building_type.append(temp[5])
    area.append(temp[6].strip('متر'))
    bedrooms.append(temp[7].strip('خواب'))

urls = [elem.get_attribute('href') for elem in ch.find_elements(By.XPATH, '//a[contains(@href, "detail")]')]
ad_id = [int(elem.get_attribute('href').split('/')[-1]) for elem in
         ch.find_elements(By.XPATH, '//a[contains(@href, "detail")]')]

for ind, item in enumerate(published_time):
    temp = item.split(' ')
    if temp[1] == 'ساعت':
        delta = datetime.timedelta(hours=int(temp[0]))
    elif temp[1] == 'روز':
        delta = datetime.timedelta(days=int(temp[0]))
    elif temp[1] == 'ماه':
        delta = datetime.timedelta(days=30)
    else:
        delta = datetime.timedelta(hours=0)
    published_time[ind] = (datetime.datetime.utcnow() - delta).strftime('%d-%m-%y')

for ind, item in enumerate(price):
    temp = item.split(' ')
    if temp[2] == 'میلیارد':
        price[ind] = float(temp[1]) * 1000
    elif temp[1] == 'میلیون':
        price[ind] = float(temp[1])

for ind, item in enumerate(area):
    temp = item.split(' ')
    area[ind] = int(temp[0])

for ind, item in enumerate(bedrooms):
    temp = item.split(' ')
    bedrooms[ind] = int(temp[0])

# TODO: careful about not overwriting existing rows
for ind, item in enumerate(ad_id):
    insert_query = 'INSERT INTO details VALUES ({}, "{}", "{}", {}, "{}", {}, {}, "{}", "{}", {}, "{}")'.format\
        (item, published_time[ind], description[ind], price[ind], location[ind],
         area[ind], bedrooms[ind], urls[ind], agency[ind], 10, building_type[ind])
    cursor.execute(insert_query)

db.commit()
cursor.close()
db.close()

