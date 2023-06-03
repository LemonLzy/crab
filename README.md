> 基于open_cv的滑动防水墙解决方案。

### 背景

螃蟹提货卡图片的账号不清晰，导致拿到提货密码后，无法输入正确的账号提货。由于查询一次会触发防水墙，所以需要一个自动化的方案。
![water_wall.png](img/water_wall.png)

可以通过selenium+open_cv，来自动尝试所有的账号+已知的密码，达到成功提货的目的。

### 环境准备

- opencv-python==3.4.3.18
- windows环境

### 结果

![crab.gif](img/crab.gif)