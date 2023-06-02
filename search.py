import random
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from crab import Crab
from utils.graph import Graph


class Search(Crab):
    def __init__(self):
        super().__init__()
        self.url = "http://xrj.360xie.cn/"

    def run(self, no):
        self.pre_attach()
        self.process_no(no)
        slide_dis = Graph(self.__class__.__name__).run(self.driver)
        self.slide(slide_dis)
        self.driver.close()

    def pre_attach(self):
        self.driver.get(self.url)

        # 确认alert弹窗
        alert = self.driver.switch_to.alert
        if alert:
            alert.accept()
            self.driver.switch_to.default_content()

        # 确认本站公告
        a_next = self.driver.find_element(By.ID, 'aNext')
        if a_next:
            a_next.click()

        # 跳转至查询页面
        self.driver.find_element(By.ID, 'checkp').click()

    def process_no(self, no):
        """
        查询页面，输入卡号查询
        """
        card_no = self.driver.find_element(By.ID, 'txtCardNo')
        card_no.send_keys(no)
        btn_search = self.driver.find_element(By.ID, 'btnSearch')
        btn_search.click()

    def slide(self, slide_dis: int):
        """
        滑动滑块
        """
        slid_ing = self.driver.find_element(By.XPATH, '//*[@id="captcha"]/div[2]/div/div')  # 滑块
        ActionChains(self.driver).click_and_hold(on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
        time.sleep(0.2)
        # print('第二步,拖动元素')
        ActionChains(self.driver).move_by_offset(xoffset=slide_dis, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform()  # 微调，根据实际情况微调
        time.sleep(0.2)
        # print('第三步,释放鼠标')
        ActionChains(self.driver).release(on_element=slid_ing).perform()
        time.sleep(2)


if __name__ == '__main__':
    s = Search()
    # print(s.__class__.__name__)
    s.run(112312312)
