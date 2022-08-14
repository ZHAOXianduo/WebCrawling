import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL_Lmao = "https://www.maoyan.com/films?yearId=16&showType=3&sortId=3"

browser = webdriver.Chrome()
browser.get(URL_Lmao)
browser.wait = WebDriverWait(browser, 30)
cur_url = browser.current_url
browser.maximize_window()
print(cur_url)
if cur_url[8:14] == 'verify':
    print('verify')

    #button = browser.wait.until(EC.element_to_be_clickable((By.ID,'tcaptcha_drag_button')))
    #button.click()

    frame = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH, '// *[ @ id = "tcaptcha_iframe"]')))
    print(frame[0])
    browser.switch_to.default_content()
    browser.switch_to_frame(frame[0])
    img = browser.wait.until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/img[1]')))
    #img = browser.find_elements_by_xpath('/html/body/div')
    print(len(img))
    print(img)
    img_ = img[0]
    location = img_.location
    size = img_.size
    print(location,size)
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
    print(left,bottom,top,right)
    screenshot = browser.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))
    captcha = screenshot.crop((747,297,1172,540))
    #747,297,1172,540
    #793,275
    captcha.show()
    browser.close()

else:
    print('crawl')
    #browser.close()