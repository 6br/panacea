import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

condition = {
    "image/fig4a.png": "http://user:pass@0.0.0.0:8080/?preset=fig4a",
    "image/fig4b.png": "http://user:pass@0.0.0.0:8080/?preset=fig4b",
    "image/fig4c.png": "http://user:pass@0.0.0.0:8080/?preset=fig4c",
    "image/fig3.png": "http://user:pass@0.0.0.0:8080/?preset=default"
}

timelapse = {
    "image/fig1/": "http://user:pass@0.0.0.0:8080/?preset=fig1",
    "image/fig5/": "http://user:pass@0.0.0.0:8080/?preset=fig5",
    "image/fig6/": "http://user:pass@0.0.0.0:8080/?preset=fig6"
}

def save(file, url, isMultiple): 
    # set driver and url
    # https://qiita.com/hujuu/items/ef89c34fca955cc571ec
    driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
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
    # File Name
    if isMultiple:
        for i in range(0, 20):
            FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), file + str(i) + ".png")

            driver.save_screenshot(FILENAME)

            time.sleep(0.5)

    else:
        FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

        driver.save_screenshot(FILENAME)

    # Close Web Browser
    driver.quit()

for (k, v) in condition.items():
    save(k, v, false)

for (k, v) in timelapse.items():
    save(k, v, false)