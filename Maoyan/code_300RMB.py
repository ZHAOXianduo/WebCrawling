import cv2
import time
from selenium import webdriver
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

class Verify_Code(object):
    """初始化webdriver"""
    def __init__(self,url):
        # self.option = webdriver.ChromeOptions()
        # self.option.add_argument('--headless')  # 设置option
        # self.driver = webdriver.Chrome()

        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(2)
        self.get_img()

    """获取背景图和缺口图"""
    def get_img(self):
        self.driver.switch_to.frame("tcaptcha_iframe")
        big_img = self.driver.find_element(By.ID, "slideBg").get_attribute("src")
        lit_img = self.driver.find_element(By.ID, "slideBlock").get_attribute("src")
        ActionChains(self.driver).release().perform()
        urlretrieve(big_img, "all_image.jpg")
        urlretrieve(lit_img, "lit_image.jpg")
        self.get_x()

    """获取滑块到缺口的距离"""
    def get_x(self):
        bg_img = cv2.imread('all_image.jpg')  # 背景图片
        tp_img = cv2.imread('lit_image.jpg')  # 缺口图片
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配
        X = max_loc[0] / 2  - 26
        self.move_slider(X)

    """滑动滑块"""
    def move_slider(self,X):
        tcaptcha = self.driver.find_element(By.ID, 'tcaptcha_drag_thumb')
        ActionChains(self.driver).drag_and_drop_by_offset(tcaptcha, xoffset=X, yoffset=0).perform()
        tcaptcha.click()
        time.sleep(2)
        #self.driver.quit()

if __name__ == '__main__':
    url = "http://verify.maoyan.com/verify?requestCode=1ddf8012aac5f7254a421eb173518e29vfgks#/"
    verify = Verify_Code(url)