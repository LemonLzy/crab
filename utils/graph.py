import base64
import time
import cv2

GAUSSIAN_BLUR_KERNEL_SIZE = (5, 5)
GAUSSIAN_BLUR_SIGMA_X = 0
CANNY_THRESHOLD1 = 200
CANNY_THRESHOLD2 = 450


class Graph:
    def __init__(self, source):
        self.source = source
        self.img_dir = "../img/"
        self.slide = f"{self.img_dir}{self.source}_slide.png"
        self.background = f"{self.img_dir}{self.source}_background.png"
        self.rectangle = f"{self.img_dir}{self.source}_rectangle.png"
        self.position = f"{self.img_dir}{self.source}_position.png"

    def run(self, driver):
        """
        下载图片，处理滑块
        """
        self.download(driver)
        self.pre_attach()
        self.identify_gap()

    def download(self, driver):
        """
        下载背景图片和小滑块
        """
        # 等待，避免下载图片时图片未加载完毕，导致下载图片为空
        time.sleep(2)
        # 下载滑块中的背景图
        # 数字表示第几个canvas
        js = f'''return document.getElementsByTagName("canvas")[0].toDataURL("image/png");'''
        base64str = driver.execute_script(js)
        page = base64str.split(',')[1]  # 去除前缀无用信息
        background_block = base64.b64decode(page)
        with open(self.background, "wb+") as f:
            f.write(background_block)
            f.close()
        time.sleep(1)

        # 下载小滑块图
        # 数字表示第几个canvas
        js = f'''return document.getElementsByTagName("canvas")[1].toDataURL("image/png");'''
        base64str = driver.execute_script(js)
        # 去除前缀无用信息
        page = base64str.split(',')[1]
        slide_block = base64.b64decode(page)
        with open(self.slide, "wb+") as f:
            f.write(slide_block)
            f.close()

    def pre_attach(self):
        """
        处理滑块图像，便于后续计算滑动距离
        """
        # 读取原图
        image_raw = cv2.imread(self.slide)
        image_height, image_width, _ = image_raw.shape

        # 高斯滤波,把一张图像变得模糊化，减少一些图像噪声干扰
        image_gaussian_blur = self.get_gaussian_blur_image(image_raw)
        cv2.imwrite(f'{self.img_dir}{self.source}_gaussian_blur.png', image_gaussian_blur)
        # Canny边缘检测
        image_canny = self.get_canny_image(image_gaussian_blur)
        cv2.imwrite(f'{self.img_dir}{self.source}_canny.png', image_canny)
        # 轮廓提取
        contours = self.get_contours(image_canny)

        y_tmp = 1000
        for contour in contours:
            x, y, w, h, = cv2.boundingRect(contour)
            if y < y_tmp:
                y_tmp = y

        # 确定滑块四个角的坐标
        tl = (1, y_tmp)  # 左上角点的坐标
        br = (63, y_tmp + 62)  # 右下角点的坐标
        tr = (63, y_tmp)
        bl = (1, y_tmp + 62)

        crop = image_raw[int(tr[1]):int(bl[1]), int(tl[0]):int(br[0])]
        cv2.rectangle(image_raw, tl, br, (0, 0, 255), 2)  # 绘制矩形
        # 保存绘制矩形后的图片
        cv2.imwrite(self.rectangle, crop)

    def identify_gap(self):
        """
        bg: 背景图片
        tp: 处理过后的缺口图片
        out:输出图片
        """
        # 读取背景图片和缺口图片
        bg_img = cv2.imread(self.background)  # 背景图片
        tp_img = cv2.imread(self.rectangle)  # 缺口图片

        # 识别图片边缘
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)

        # 转换图片格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        # 缺口匹配
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        # 绘制方框
        th, tw = tp_pic.shape[:2]
        # print(th, tw)
        tl = max_loc  # 左上角点的坐标
        # print(tl)
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite(self.position, bg_img)  # 保存在本地

        # 返回缺口的X坐标
        print("缺口的x坐标是：", tl[0])
        return tl[0]

    def get_gaussian_blur_image(self, image):
        # def GaussianBlur(src, ksize, sigmaX, dst=None, sigmaY=None, borderType=None)
        # src：即需要被处理的图像。ksize：进行高斯滤波处理所用的高斯内核大小，它需要是一个元组，包含 x 和 y 两个维度
        # sigmaX：表示高斯核函数在 X 方向的的标准偏差。
        # sigmaY：表示高斯核函数在 Y 方向的的标准偏差，若 sigmaY 为 0，就将它设为 sigmaX，如果 sigmaX 和 sigmaY 都是 0，那么 sigmaX 和 sigmaY 就通过 ksize 计算得出
        return cv2.GaussianBlur(image, GAUSSIAN_BLUR_KERNEL_SIZE, GAUSSIAN_BLUR_SIGMA_X)

    def get_canny_image(self, image):
        return cv2.Canny(image, CANNY_THRESHOLD1, CANNY_THRESHOLD2)

    def get_contours(self, image):
        # OpenCV3中：则会返回三个值：处理的图像(image)轮廓的点集(contours)各层轮廓的索引(hierarchy)
        image, contours, hierarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        return contours


if __name__ == '__main__':
    g = Graph("search")
    g.pre_attach()
