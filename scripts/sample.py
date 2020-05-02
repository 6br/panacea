import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# File Name
FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image/screen.png")

# set driver and url
# https://qiita.com/hujuu/items/ef89c34fca955cc571ec
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
url = 'http://user:pass@0.0.0.0:8080/?preset=default'
driver.get(url)
#time.sleep(5)

# get width and height of the page
w = driver.execute_script("return document.body.scrollWidth;")
h = driver.execute_script("return document.body.scrollHeight;")

# set window size
driver.set_window_size(w,h)

element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id("contentsLoaded"))

time.sleep(2)

# Get Screen Shot
driver.save_screenshot(FILENAME)

# Close Web Browser
driver.quit()