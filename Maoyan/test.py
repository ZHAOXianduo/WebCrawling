from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import cv2
from selenium.webdriver import ActionChains
import requests
from io import BytesIO


class MaoYanCode(object):
    # 初始化
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset=100'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 10)

    def open(self):
        # 打开网页
        self.browser.get(self.url)

    # 定位背景图
    def bg_img_src(self):
        bg_img_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@class="tc-bg"]/img')))
        bg_img_src = bg_img_element.get_attribute('src')
        return bg_img_src

    # 定位缺块
    def jpp_img_src(self):
        target_img_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@class="tc-jpp"]/img')))
        target_img_src = target_img_element.get_attribute('src')
        return target_img_src

    # 获取背景和缺块图片
    def get_img(self):
        bg_src = self.bg_img_src()
        jpp_src = self.jpp_img_src()
        response1 = requests.get(bg_src)
        image1 = Image.open(BytesIO(response1.content))
        image1.save('bg_img.png')
        response2 = requests.get(jpp_src)
        image2 = Image.open(BytesIO(response2.content))
        image2.save('jpp_img.png')
        return image1, image2

    # 定位滑块
    def slider_element(self):
        time.sleep(2)
        slider = self.wait.until(EC.presence_of_element_located(
            (By.XPATH,
             '//*[@class="tc-drag-thumb"]')))
        return slider

    # 识别缺口
    def get_gap(self, gap_img):
        bg_img = cv2.imread('bg_img.png')
        tp_img = cv2.imread('jpp_img.png')

        # 识别图片边缘
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)

        # 转换图片格式
        # 灰度图片转为RGB彩色图片
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        # 缺口匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        # 绘制方框
        # img.shape[:2] 获取图片的长、宽
        height, width = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        cv2.rectangle(bg_img, tl, (tl[0] + width - 15, tl[1] + height - 15),
                      (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite(gap_img, bg_img)  # 保存在本地
        # 返回缺口的X坐标
        return tl[0]

    # 构造移动轨迹
    def get_track(self, distance):
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正5
                a = 5
            else:
                # 加速度为负3
                a = -3
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    # 移动滑块
    def move_to_gap(self, slider, track):
        # click_and_hold()按住底部滑块
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x,
                                                      yoffset=0).perform()
        ActionChains(self.browser).release().perform()

    def login(self):
        self.open()
        time.sleep(2)
        iframe = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(iframe[1]))
        self.get_img()
        slider = self.slider_element()
        slider.click()
        gap = self.get_gap('result.png')
        # 页面为360*360,图片为680*390,更改比例,减去初始位移
        gap_end = int((gap - 40) / 2)
        # 获取缺口
        print('缺口位置', gap_end)
        # 减去缺块白边
        gap_end -= 10
        # 获取移动轨迹
        track = self.get_track(gap_end)
        print('滑动轨迹', track)
        # 拖动滑块
        self.move_to_gap(slider, track)


if __name__ == '__main__':
    crack = MaoYanCode()
    crack.login()