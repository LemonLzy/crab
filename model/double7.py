from selenium.common import NoSuchElementException

from selenium.webdriver.common.by import By

from model.waterfall import WaterFull
from utils.graph import Graph


class DoubleZero7(WaterFull):
    """
    腾讯防水墙滑动验证码破解
    使用OpenCV库
    成功率大概90%左右：在实际应用中，登录后可判断当前页面是否有登录成功才会出现的信息：比如用户名等。循环
    https://open.captcha.qq.com/online.html
    破解 腾讯滑动验证码
    腾讯防水墙
    python + seleniuum + cv2
    """

    def __init__(self):
        super().__init__()
        self.url = "https://007.qq.com/"
        self.btn_search_id = "code"
        self.slide_block_xpath = "//div[@id=\"tcaptcha_drag_thumb\"]"

    def run(self, no=None):
        self.pre_attach()
        slide_dis = Graph(self.__class__.__name__).run(self.driver)
        self.slide(slide_dis)
        self.driver.close()

    def pre_attach(self):
        # 点击体验验证码
        try:
            a_next = self.driver.find_element(By.ID, self.btn_search_id)
            if a_next:
                a_next.click()
        except NoSuchElementException:
            print("code has not found.")
            return

        # 切换到滑块frame
        self.driver.switch_to.frame(self.driver.find_element(By.ID, 'tcaptcha_iframe'))


if __name__ == '__main__':
    phone = "****"
    double7 = DoubleZero7()
    double7.run()
