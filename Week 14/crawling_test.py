from selenium import webdriver
import sqlite3
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains

ch = webdriver.Chrome(ChromeDriverManager().install())

url = "https://kilid.com/buy/tehran-satarkhan?listingTypeId=1&location=328363&sort=DATE_DESC&page=0"
ch.maximize_window()
ch.get(url)

time.sleep(2)

urls = [elem.get_attribute('href') for elem in ch.find_elements(By.XPATH, '//a[contains(@href, "detail")]')]
for u in urls:
    ch.get(u)
    button = ch.find_element(By.CLASS_NAME, 'single-sticky__button--call')
    # ActionChains(ch).move_to_element(button).click(button).perform()
    # ch.implicitly_wait(10)

    button.click()  # ---> selenium.common.exceptions.ElementNotInteractableException:
    time.sleep(2)
    print(button.text)







