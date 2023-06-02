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
        Graph(self.__class__.__name__).run(self.driver)

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


if __name__ == '__main__':
    s = Search()
    # print(s.__class__.__name__)
    s.run(112312312)
