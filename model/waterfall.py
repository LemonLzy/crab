import random
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from utils.driver import driver
from utils.graph import Graph


class WaterFull:
    """ 防水墙滑动验证码破解 使用OpenCV库 成功率大概90%左右"""

    def __init__(self):
        # 提货平台官网
        self.url = "http://xrj.360xie.cn"
        self.driver = driver
        self.driver.implicitly_wait(5)
        self.card_no_id = "txtCardNo"
        self.btn_search_id = "btnSearch"
        self.slide_block_xpath = "//*[@id=\"captcha\"]/div[2]/div/div"

    def run(self, no):
        self.pre_attach()
        self.process_no(no)
        slide_dis = Graph(self.__class__.__name__).run(self.driver)
        self.slide(slide_dis)
        self.driver.close()

    @staticmethod
    def get_track(distance):
        """ 模拟轨迹 假装是人在操作"""
        # 初速度
        v = 1
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.2
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 7 / 8
        distance += 10  # 先滑过一点，最后再反着滑动回来
        # a = random.randint(1,3)
        while current < distance:
            # if current < mid:
            #     # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            #     a = random.randint(2, 4)  # 加速运动
            # else:
            #     a = -random.randint(3, 5)  # 减速运动

            a = random.randint(2, 4)
            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 2 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))
            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        # 反着滑动到大概准确位置
        for i in range(4):
            tracks.append(-random.randint(2, 3))
        for i in range(4):
            tracks.append(-random.randint(1, 3))
        return tracks

    def pre_attach(self):
        self.driver.get(self.url)

        # 确认alert弹窗
        alert = self.driver.switch_to.alert
        if alert:
            alert.accept()
            self.driver.switch_to.default_content()

        # 确认本站公告
        try:
            a_next = self.driver.find_element(By.ID, 'aNext')
            if a_next:
                a_next.click()
        except NoSuchElementException:
            print("a_next has not found.")
            pass

    def process_no(self, no):
        """
        输入卡号，点击查询
        """
        card_no = self.driver.find_element(By.ID, self.card_no_id)
        card_no.send_keys(no)
        btn_search = self.driver.find_element(By.ID, self.btn_search_id)
        btn_search.click()

    def slide(self, slide_dis: int):
        """
        滑动滑块
        """
        slide_block = self.driver.find_element(By.XPATH, self.slide_block_xpath)

        # 点击鼠标左键，按住不放
        ActionChains(self.driver).click_and_hold(on_element=slide_block).perform()
        time.sleep(0.2)
        # print('第二步,拖动元素')
        ActionChains(self.driver).move_by_offset(xoffset=slide_dis, yoffset=0).perform()
        # 微调，根据实际情况微调
        ActionChains(self.driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform()
        time.sleep(0.2)
        # print('第三步,释放鼠标')
        ActionChains(self.driver).release(on_element=slide_block).perform()
        time.sleep(2)
