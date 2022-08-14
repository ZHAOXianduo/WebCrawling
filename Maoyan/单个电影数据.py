from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
### 设置请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Cookie': '__mta=244235578.1650771731530.1650791894282.1650791939343.15; uuid_n_v=v1; uuid=9DE714C0C38011ECB8911B64CB177626C253C60A20674BAFAC1DE9D26F45C30A; _lxsdk_cuid=18059a8e69cc8-082db4508ae269-3e604809-1fa400-18059a8e69cc8; _csrf=c1e5a036f56f0d19afd296371e29255c4cfd81de89dcfe4a9d1eaee260943856; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1650771731; Cc2838679FS=5QADdWygLWQ8lFqnrHs4BFsQplh8ohMVH7xSHGIpJUzLmrh2tTXOS52ItRCXENY6YOcq2qGP2u60DRpUhkKMp3q; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; _lxsdk=9DE714C0C38011ECB8911B64CB177626C253C60A20674BAFAC1DE9D26F45C30A; __utma=17099173.2097531496.1650772129.1650772129.1650772129.1; __utmc=17099173; __utmz=17099173.1650772129.1.1.utmcsr=so.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; Cc2838679FT=63bsE5Cx9ntqqqqDqKMlQvGyhWEeEGeBIz3bUNvP5dtzXrcUBuMCTs7C_WidBm.DxbTWWulqN_Am9UjR3xKoikCpgS5ZR0pS00HzQ_FqnH1Uyp0U6qO3FJab6FJPyoOwnpvn6xU3T57Rfx8a6GJIJlWdvLzYaInJBMITiU475O_Oa; __mta=244235578.1650771731530.1650791796416.1650791934713.15; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1650791939; _lxsdk_s=1805adacdd3-039-775-d0%7C%7C22'}
### 2021年电影猫耳列表

URL_Lmao = "https://www.maoyan.com/films?yearId=16&showType=3&sortId=3"

browser = webdriver.Chrome()
browser.wait = WebDriverWait(browser, 30)
browser.get(URL_Lmao)
infor = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/h1/span')
print(infor.text)
#button = browser.wait.until(EC.element_to_be_clickable((By.ID,'reload-button')))
#button.click()
#url = browser.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div[2]/dl/dd[1]/div[1]/a')
#//*[@id="app"]/div/div[2]/div[2]/dl/dd[2]/div[1]/a
#主要改dd[x]
#url_ = url[0].get_attribute('href')
#browser.get(url_)
