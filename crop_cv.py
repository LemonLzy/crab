import cv2

GAUSSIAN_BLUR_KERNEL_SIZE = (5, 5)
GAUSSIAN_BLUR_SIGMA_X = 0
CANNY_THRESHOLD1 = 200
CANNY_THRESHOLD2 = 450


# cv2识别滑块验证中的缺口：https://blog.csdn.net/zhangzeyuaaa/article/details/119508407
# cv2图像匹配识别滑动验证码缺口：https://blog.csdn.net/qq_44033208/article/details/125147352
# cv2根据坐标点截图：https://blog.csdn.net/weixin_43134049/article/details/110914634

def get_gaussian_blur_image(image):
    # def GaussianBlur(src, ksize, sigmaX, dst=None, sigmaY=None, borderType=None)
    # src：即需要被处理的图像。ksize：进行高斯滤波处理所用的高斯内核大小，它需要是一个元组，包含 x 和 y 两个维度
    # sigmaX：表示高斯核函数在 X 方向的的标准偏差。
    # sigmaY：表示高斯核函数在 Y 方向的的标准偏差，若 sigmaY 为 0，就将它设为 sigmaX，如果 sigmaX 和 sigmaY 都是 0，那么 sigmaX 和 sigmaY 就通过 ksize 计算得出
    return cv2.GaussianBlur(image, GAUSSIAN_BLUR_KERNEL_SIZE, GAUSSIAN_BLUR_SIGMA_X)


def get_canny_image(image):
    return cv2.Canny(image, CANNY_THRESHOLD1, CANNY_THRESHOLD2)


def get_contours(image):
    # OpenCV3中：则会返回三个值：处理的图像(image)轮廓的点集(contours)各层轮廓的索引(hierarchy)
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def main():
    # 读取原图
    image_raw = cv2.imread('crabCV/search_slide.png')
    image_height, image_width, _ = image_raw.shape
    # print(image_height, image_width, _)  # 320 520 3
    # 高斯滤波,把一张图像变得模糊化，减少一些图像噪声干扰
    image_gaussian_blur = get_gaussian_blur_image(image_raw)
    cv2.imwrite('./image/image_gaussian_blur.png', image_gaussian_blur)
    # Canny边缘检测
    image_canny = get_canny_image(image_gaussian_blur)
    cv2.imwrite('./image/image_canny.png', image_canny)
    # 轮廓提取
    contours = get_contours(image_canny)

    y_tmp = 1000
    for contour in contours:
        x, y, w, h, = cv2.boundingRect(contour)
        # print(x, y, w, h)
        if y < y_tmp:
            y_tmp = y

    # print(y_tmp)
    # 确定滑块四个角的坐标
    tl = (1, y_tmp)  # 左上角点的坐标
    br = (63, y_tmp + 62)  # 右下角点的坐标
    tr = (63, y_tmp)
    bl = (1, y_tmp + 62)

    crop = image_raw[int(tr[1]):int(bl[1]), int(tl[0]):int(br[0])]

    # cv2.rectangle(image_raw, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite("./image/tp.png", crop)  # 保存在本地


if __name__ == '__main__':
    main()
