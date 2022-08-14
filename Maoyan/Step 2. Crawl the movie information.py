import cv2
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""获取背景图和缺口图"""
def get_img(driver):
    #frame = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '// *[ @ id = "tcaptcha_iframe"]')))
    #driver.switch_to.frame(frame[0])
    driver.switch_to.frame("tcaptcha_iframe")
    big_img = driver.find_element(By.ID, "slideBg").get_attribute("src")
    lit_img = driver.find_element(By.ID, "slideBlock").get_attribute("src")
    ActionChains(driver).release().perform()
    urlretrieve(big_img, "all_image.jpg")
    urlretrieve(lit_img, "lit_image.jpg")
    get_x(driver)

"""获取滑块到缺口的距离"""
def get_x(driver):
    bg_img = cv2.imread('all_image.jpg')  # 背景图片
    tp_img = cv2.imread('lit_image.jpg')  # 缺口图片
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
    X = max_loc[0] / 2  - 26
    move_slider(driver,X)

    """滑动滑块"""
def move_slider(driver,X):
    #tcaptcha = driver.find_element(By.ID, 'tcaptcha_drag_thumb')
    #ActionChains(driver).drag_and_drop_by_offset(tcaptcha, xoffset=X/2, yoffset=0).perform()
    #time.sleep(1)
    #ActionChains(driver).drag_and_drop_by_offset(tcaptcha, xoffset=X/2, yoffset=0).perform()
    #tcaptcha.click()
    #time.sleep(2)
    tcaptcha = driver.find_element(By.ID, 'tcaptcha_drag_thumb')
    ActionChains(driver).drag_and_drop_by_offset(tcaptcha, xoffset=X, yoffset=0).perform()
    tcaptcha.click()
    time.sleep(2)
    #self.driver.quit()

def page(cur_url):
    if 'verify' in cur_url:
        print('verify')
        get_img(browser)
        return 'verify'
    else:
        infor = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/h1/span')
        if infor.text == '该网页无法正常运作':
            print('refresh')
            button = browser.wait.until(EC.element_to_be_clickable((By.ID, 'reload-button')))
            button.click()
            return 'refresh'
        else:
            print('crawl')
            return 'crawl'

def name_score(str_):
    for i in range(len(str_)):
        if i % 2 == 0:
            Name_.append(str_[i])
        else:
            Score_.append(str_[i])
    return 0

def name_url(url_):
    URL_.append(url_)
    return 0

for i in range(67):#67
    Name_ = []
    Score_ = []
    URL_ = []
    print((i+1)/100*100,'%')
    URL_Lmao = "https://www.maoyan.com/films?showType=3&sortId=3&offset="+str((i)*30)
    browser = webdriver.Chrome()
    browser.wait = WebDriverWait(browser, 30)
    browser.get(URL_Lmao)
    browser.maximize_window()
    cur_url = browser.current_url
    time.sleep(2)
    page(cur_url)
    while cur_url != URL_Lmao:
        print(cur_url)
        ret = page(cur_url)
        if ret == 'verify':
            time.sleep(5)
        else:
            time.sleep(2)
        cur_url = browser.current_url
    firms = browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[2]/dl')
    firm_info = firms.text.split('\n')
    name_score(firm_info)
    for k in range(30):
        xpath_ = '/html/body/div[4]/div/div[2]/div[2]/dl/dd[' + str(k + 1) + ']/div[1]/a'
        url = browser.find_element_by_xpath(xpath_)
        URL_L = url.get_attribute('href')
        name_url(URL_L)
    df = pd.DataFrame({
        'Firm': Name_,
        'Score': Score_,
        'URL': URL_
    })
    df.to_excel('Firm_List_' + str(i + 1) + '.xlsx')
    browser.close()







#URL_Lmao = "https://www.maoyan.com/films?yearId=16&showType=3&sortId=3&offset=0"
#browser = webdriver.Chrome()
#browser.wait = WebDriverWait(browser, 30)
#browser.get(URL_Lmao)
#browser.maximize_window()
#cur_url = browser.current_url
#time.sleep(2)
#page(cur_url)
#while cur_url != URL_Lmao:
#    print(cur_url)
#    page(cur_url)
#    time.sleep(2)
#    cur_url = browser.current_url
#firms = browser.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[2]/dl')
#print(firms.text)
#print(type(firms.text))
#for i in range(30):
#    xpath_ = '/html/body/div[4]/div/div[2]/div[2]/dl/dd['+str(i+1)+']/div[1]/a'
#    url = browser.find_element_by_xpath(xpath_)
##/html/body/div[4]/div/div[2]/div[2]/dl/dd[1]/div[1]/a
##/html/body/div[4]/div/div[2]/div[2]/dl/dd[2]/div[1]/a
##/html/body/div[4]/div/div[2]/div[2]/dl/dd[30]/div[1]/a
#    print(url.get_attribute('href'))