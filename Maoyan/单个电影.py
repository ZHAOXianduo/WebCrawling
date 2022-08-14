import cv2
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

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
#option=webdriver.ChromeOptions()
#option.binary_location=r'D:\Program Files (x86)\360se6\Application\360se.exe'
URL_Lmao = "https://www.maoyan.com/films/1277939"
#browser = webdriver.Chrome(r'D:\Program Files (x86)\360se6\Application\360se.exe',options=option)
#__browser_url = r'D:\Program Files (x86)\360se6\Application\360se.exe'  ##360浏览器的地址
chrome_options = Options()
#chrome_options.binary_location = __browser_url
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(chrome_options=chrome_options)
#browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#    "source": """
#    Object.defineProperty(navigator, 'webdriver', {
#      get: () => undefined
#    })
#  """
#})
#browser = webdriver.Chrome(options=option)
browser.wait = WebDriverWait(browser, 30)
browser.get(URL_Lmao)
browser.maximize_window()
cur_url = browser.current_url
time.sleep(2)
page(cur_url)
#/html/body/div[3]/div/div[1]/div/div/i
###抓取电影类型 比如imax2d--一些电影没有，因此需要去判断/html/body/div[3]/div/div[1]/div/div路径是否存在子集
#ver_ = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div[1]/div/div/i')))[0].get_attribute('class')
##ver_ = browser.find_element_by_xpath('#/html/body/div[3]/div/div[1]/div/div/i').get_attribute('class')
##/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a
##type_ = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/a')))[0].get_attribute('text')
##/html/body/div[3]/div/div[2]/div[1]/ul/li[2]
###抓取电影基本信息：电影类型，制作国家，电影市场，上映时间
#info = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/ul')))[0].text
##/html/body/div[3]/div/div[2]/div[3]
#评分数据和点评数据
#score = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div[2]/div[3]')))[0].text
#print(score.split('\n'))
#//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[1]/div[2]
#抓取剧情简介
#story = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[1]/div[2]')))[0].text
#抓取获奖信息
#//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[3]/div[2]/ul
#reward = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[3]/div[2]/ul')))[0].text
#print(reward)
#抓取影片资料 比如需不需要家长引导，出品发行方，技术参数
#record = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[1]/div/div[3]/div[1]/div[6]')))[0].text
#/html/body/div[4]/div/div[1]/div/div[3]/div[1]/div[6]
#print(record)
#荣誉奖项其他参数
#/html/body/div[4]/div/div[1]/div/div[3]/div[1]/div[7]
#reward_count = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[1]/div/div[3]/div[1]/div[7]')))[0].text
#print(reward_count)
#电影原声，是否有
#/html/body/div[4]/div/div[1]/div/div[3]/div[1]/div[9]
#相关电影
#/html/body/div[4]/div/div[2]/div/div[3]/div[2]/div/dl
#relative = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[3]/div[2]/div/dl')))[0].text
#print(relative)
#预告片-最高播放量 -- 抓取伪元素
#/html/body/div[4]/div/div[2]/div/div[2]/div[1]/div/div[2]/div
##relative = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/div[1]/div/div[2]/div/ul/li[1]/div/div[2]/div/span')))[0].text
#relative = browser.find_element_by_css_selector("#app > div > div.related > div > div.tab-content-container > div.tab-preview.tab-content.active > div > div.mod-content > div > ul > li:nth-child(1) > div > div.top5-video-info > div").text
#print(relative)
#点击演员数据表 -- 点击伪元素
#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(2)
#点击成功，靠谱~
#button_actor = browser.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(2)')))
#button_actor.click()