import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# File Name
FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image/screen.png")

# set driver and url
# https://qiita.com/hujuu/items/ef89c34fca955cc571ec
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
url = 'http://user:pass@0.0.0.0:8080/?preset=default'
driver.get(url)
driver.set_page_load_timeout(10)
#time.sleep(5)

# get width and height of the page
w = driver.execute_script("return document.body.scrollWidth;")
h = driver.execute_script("return document.body.scrollHeight;")

# set window size
driver.set_window_size(w,h)

time.sleep(2)

element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'contentsLoaded')))

time.sleep(2)

# Get Screen Shot
driver.save_screenshot(FILENAME)

# Close Web Browser
driver.quit()