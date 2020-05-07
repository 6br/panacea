import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

condition = {
    "image/fig3a.png": "http://user:pass@0.0.0.0:8080/?preset=Fig4a",
    "image/fig3b.png": "http://user:pass@0.0.0.0:8080/?preset=Fig4b",
    "image/fig3c.png": "http://user:pass@0.0.0.0:8080/?preset=Fig4c",
    "image/fig2.png": "http://user:pass@0.0.0.0:8080/?preset=Default"
}

timelapse = {
    "image/fig1_4/": "http://user:pass@0.0.0.0:8080/?preset=Fig1",
    "image/fig5/": "http://user:pass@0.0.0.0:8080/?preset=Fig5",
    "image/fig6/": "http://user:pass@0.0.0.0:8080/?preset=Fig6"
}

def save_png(driver, file, url, isMultiple): 
    # set driver and url
    # https://qiita.com/hujuu/items/ef89c34fca955cc571ec
    
    driver.get(url)
    #time.sleep(5)

    # get width and height of the page
    w = driver.execute_script("return document.body.scrollWidth;")
    h = driver.execute_script("return document.body.scrollHeight;")

    # set window size
    driver.set_window_size(w,h)

    time.sleep(2)

    element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'contentsLoaded')))

    # Get Screen Shot
    # File Name
    if isMultiple:
        os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), file))
        for i in range(0, 20):
            FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), file + str(i) + ".png")

            driver.save_screenshot(FILENAME)

            time.sleep(0.5)

    else:
        time.sleep(12)

        FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

        driver.save_screenshot(FILENAME)

def driverfunc(k, v, arg):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver' )
    #driver.maximize_window()
    driver.set_window_size(1920, 1080) # Full hd
    driver.set_page_load_timeout(20)
    save_png(driver, k, v, arg)
    driver.quit()

executor = ThreadPoolExecutor(max_workers=2)
for (k, v) in condition.items():
    #save_png(driver, k, v, False)
    executor.submit(driverfunc, k, v, False)

for (k, v) in timelapse.items():
    #save_png(driver, k, v, True)
    executor.submit(driverfunc, k, v, True)

# Close Web Browser
#driver.quit()

# 並列実行するexecutorを用意する。
# max_workers が最大の並列実行数

#for t in testcase:
#    executor.submit(driverfunc,t)