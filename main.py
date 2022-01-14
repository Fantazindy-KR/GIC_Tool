from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
import urllib.request
from multiprocessing import Pool
import pandas as pd

key = pd.read_csv('./keyword.txt', encoding='cp949', names=['keyword'])
# add your searching keyword in keyword.txt file and put in same diretory with this file
keyword = []
[keyword.append(key['keyword'][x]) for x in range(len(key))]


def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error : Failed to create target directory")


def image_download(keyword):
    createDirectory('./' + keyword + '_high resolution')

    chromedriver = 'C://chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    driver.implicitly_wait(3)

    print(keyword, 'Search')
    driver.get('https://www.google.co.kr/imghp?hl=ko')

    Keyword = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    Keyword.send_keys(keyword)

    driver.find_element_by_xpath('//*[@id="sbtc"]/button').click()

    print(keyword + ' Scrolling .............')
    elem = driver.find_element_by_tag_name("body")
    for i in range(60):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[4]/div[2]/input').click()
        for i in range(60):
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.1)
    except:
        pass

    images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")
    print(keyword + ' Found img count:', len(images))

    links = []
    for i in range(1, len(images)):
        try:
            driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img').click()
            links.append(driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img').get_attribute(
                'src'))
            driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[2]/a').click()
            print(keyword + ' Gathering link..... number :' + str(i) + '/' + str(len(images)))
        except:
            continue

    forbidden = 0
    for k, i in enumerate(links):
        try:
            url = i
            start = time.time()
            urllib.request.urlretrieve(url, "./" + keyword + "_high resolution/" + keyword + "_" + str(
                k - forbidden) + ".jpg")
            print(str(k + 1) + '/' + str(len(links)) + ' ' + keyword + ' Downloading....... Download time : ' + str(
                time.time() - start)[:5] + ' sec')
        except:
            forbidden += 1
            continue
            print(keyword + ' ---Download Compleate---')

            driver.close()


# =============================================================================
# Running code
# =============================================================================

if __name__ == '__main__':
    pool = Pool(processes=1)  # Put num of core to use
    pool.map(image_download, keyword)

