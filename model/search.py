from selenium.webdriver.common.by import By
from crab_basic import CrabBasic
from utils.graph import Graph


class Search(CrabBasic):
    def __init__(self):
        super().__init__()

    def run(self, no):
        self.pre_attach()
        # 跳转至查询页面
        self.driver.find_element(By.ID, 'checkp').click()

        self.process_no(no)
        slide_dis = Graph(self.__class__.__name__).run(self.driver)
        self.slide(slide_dis)
        self.driver.close()


if __name__ == '__main__':
    s = Search()
    # print(s.__class__.__name__)
    s.run(112312312)
