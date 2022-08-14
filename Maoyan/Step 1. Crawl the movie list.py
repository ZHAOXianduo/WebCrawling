import os
import time
import xlsxwriter
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

path = r"C:\Users\NHT\PycharmProjects\猫眼电影爬虫\电影清单"
files = os.listdir(path)
for file in files:
    print(file[:-5]+'_crawl'+'.xlsx')
    list = pd.read_excel(path+'\\'+str(file))
    list['ver_'] = ''
    list['type_of_firm'] = ''
    list['country'] = ''
    list['range'] = ''
    list['on_show'] = ''
    list['story'] = ''
    list['comment'] = ''
    list['document'] = ''
    list['sale'] = ''
    list['relative'] = ''
    list['announce_'] = ''
    list['celebrity'] = ''
    list['reward'] = ''
    list['num_photo'] = 0
    print(list)
    for i in range(len(list)):
        URL = list['URL'][i]
        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.wait = WebDriverWait(browser, 5)
        browser.get(URL)
        browser.maximize_window()
        cur_url = browser.current_url
        try:
            infor = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/h1/span')
            if infor.text == '该网页无法正常运作':
                print('refresh！')
                button = browser.wait.until(EC.element_to_be_clickable((By.ID, 'reload-button')))
                button.click()
        except:
            print('无需跳转')
        #time.sleep(1)
        try:
            button_actor = browser.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(2)')))
        except:
            button_actor = None
        try:
            button_reward = browser.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(3)')))
        except:
            button_reward = None
        try:
            button_photo = browser.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(4)')))
        except:
            button_photo = None
        if button_actor != None:
            actor_class = (button_actor.get_attribute('class'))
        else:
            actor_class = 'disabled'
        if button_reward != None:
            reward_class = (button_reward.get_attribute('class'))
        else:
            reward_class = 'disabled'
        if button_photo != None:
            photo_class = (button_photo.get_attribute('class'))
        else:
            photo_class = 'disabled'
        try:
            list['ver_'][i] = browser.find_element_by_css_selector('body > div.banner > div > div.celeInfo-left > div > div > i').get_attribute('class')
        except:
            list['ver_'][i] = ''
        try:
            info = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/ul')))[0].text
            info = info.split('\n')
            list['type_of_firm'][i] = info[0]
            list['country'][i] = info[1].split('/')[0]
            list['range'][i] = info[1].split('/')[1]
            list['on_show'][i] = info[2][0:10]
        except:
            info = ''
        #time.sleep(1)
        try:
            list['story'][i] = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[1]/div[2]')))[0].text
        except:
            list['story'][i] = ''
        j = 5
        if 'disabled' not in str(actor_class):
            j = j
        else:
            j = j - 1
        if 'disabled' not in str(photo_class):
            j = j
        else:
            j = j - 1
        if 'disabled' not in str(reward_class):
            j = j
        else:
            j = j - 1
        #time.sleep(2)
        try:
            list['comment'][i] = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[' + str(j) + ']')))[0].text
        except:
            list['comment'][i] = ''
        try:
            #list['document'][i] = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[' + str(j + 1) + ']')[0].get_attribute('class')
            list['document'][i] = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[' + str(j + 1) + ']')))[0].text
        except:
            list['document'][i] = ''
        if 'disabled' not in str(reward_class):
            j = j + 1
        else:
            j = j
        try:
            list['sale'][i] = browser.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[' + str(j + 2) + ']')))[0].text
        except:
            list['sale'][i] = ''
        try:
            list['relative'][i] = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[3]/div[2]/div/dl')))[0].text
        except:
            list['relative'][i] = ''
        try:
            list['announce_'][i] = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/div[1]/div/div[2]/div')))[0].text
        except:
            list['announce_'][i] = ''
        if 'disabled' not in str(actor_class):
            button_actor.click()
            #time.sleep(2)```````````````````*******                   ````````````````````````````````````````````````````````````````````````````````
            list['celebrity'][i] = browser.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, '/ html / body / div[4] / div / div[1] / div / div[3] / div[2] / div')))[0].text
        else:
            list['celebrity'][i] = ''
        if 'disabled' not in str(reward_class):
            button_reward.click()
            #time.sleep(2)
            list['reward'][i] = browser.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[3]')))[0].text
        else:
            list['reward'][i] = ''
        if 'disabled' not in str(photo_class):
            button_photo.click()
            #time.sleep(1)
            photo = browser.find_elements(By.CLASS_NAME, 'default-img')
            list['num_photo'][i] = len(photo)
        else:
            list['num_photo'][i] = 0
        browser.close()
        print(i)
        print(list.iloc[i])
    #print(list)
    list.to_excel(r"C:\Users\NHT\PycharmProjects\猫眼电影爬虫\\"+file[:-5]+ "_crawl"+".xlsx",encoding = 'gkb')
