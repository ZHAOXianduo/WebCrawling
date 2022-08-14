import time
from selenium import webdriver

URL_Lmao = "https://www.maoyan.com/films?showType=3&sortId=3&offset="
for i in range(67):
    url = URL_Lmao+str(i*30)
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(1)
    browser.close()