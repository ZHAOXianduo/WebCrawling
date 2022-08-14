from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

URL_Lmao = "https://www.maoyan.com/films/1383307" #"https://www.maoyan.com/films/1277939"
URL_Lmao = "https://www.maoyan.com/films/588362"
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.wait = WebDriverWait(browser, 30)
browser.get(URL_Lmao)
browser.maximize_window()
cur_url = browser.current_url
try:
    infor = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/h1/span')
except:
    print('无需跳转')
else:
    if infor.text == '该网页无法正常运作':
        print('refresh！')
        button = browser.wait.until(EC.element_to_be_clickable((By.ID, 'reload-button')))
        button.click()
# 开始抓取数据

###获取后三个主要页面信息
button_actor = browser.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(2)')))
button_reward = browser.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(3)')))
button_photo = browser.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#app > div > div.main-content > div > div.tab-title-container.clearfix > div:nth-child(4)')))
actor_class = (button_actor.get_attribute('class'))
reward_class = (button_reward.get_attribute('class'))
#print('disabled' in str(reward_class))
photo_class = (button_photo.get_attribute('class'))

###抓取介绍页的数据
###抓取电影荧幕类型 比如imax2d--一些电影没有，因此需要去判断/html/body/div[3]/div/div[1]/div/div路径是否存在子集
try:
    ver_ = browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div/i')[0].get_attribute('class')
except:
    ver_ = 'None'
#print(ver_)
###抓取电影基本信息：电影类型，制作国家，电影时长，上映时间
info = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/ul')))[0].text
info = info.split('\n')
type_of_firm = info[0]
country = info[1].split('/')[0]
range = info[1].split('/')[1]
on_show = info[2][0:10]
###抓取剧情简介
story = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div[1]/div[2]')))[0].text
###抓取热门短评，影票资料和影票票房
i = 5
if 'disabled' not in str(actor_class):
    i = i
else:
    i = i-1
if 'disabled' not in str(photo_class):
    i = i
else:
    i = i-1
if 'disabled' not in str(reward_class):
    i = i
else:
    i = i-1
comment = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div['+str(i)+']')))[0].text
#comment = comment.split('\n')[1:-1]
document = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div['+str(i+1)+']')))[0].text
#document = document.split('\n')[1:]
if 'disabled' not in str(reward_class):
    i = i+1
else:
    i = i
sale = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[1]/div['+str(i+2)+']')))[0].text


###抓取附栏页数据
###抓取相关电影
relative = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[3]/div[2]/div/dl')))[0].text
#relative = relative.split('\n')
###预告片-最高播放量 -- 抓取伪元素
announce_ = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/div[1]/div/div[2]/div')))[0].text
#announce_ = announce_.split('\n')

###跳转到演员列表
if 'disabled' not in str(actor_class):
    button_actor.click()
    celebrity = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '/ html / body / div[4] / div / div[1] / div / div[3] / div[2] / div')))[0].text
else:
    celebrity = ''

###跳转到获奖列表
if 'disabled' not in str(reward_class):
    button_reward.click()
    reward = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[1]/div/div[3]/div[3]')))[0].text
else:
    reward = ''

###跳转到图集列表
if 'disabled' not in str(photo_class):
    button_photo.click()
    photo = browser.find_elements(By.CLASS_NAME,'default-img')
    num_photo = len(photo)
else:
    num_photo = 0

print(ver_) ##银幕类型
print(type_of_firm) ##电影类型
print(country) ##制片国家
print(range) ##电影时长
print(on_show) ##上映时间
print(story) ##剧情简介
print(comment) ##热门评论
print(document) ##影片资料
print(sale) ##票房信息
print(relative) ##相关电影
print(announce_) ##预告片数据
print(celebrity) ##演员列表
print(reward) ##获奖名单
print(num_photo) ##图集数量
browser.close()