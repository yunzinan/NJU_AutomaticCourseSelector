from selenium import webdriver
import time
import os.path
import urllib.request
from chaojiying import Chaojiying_Client


def chooseSelectedCourse(courseName):
    searchTag = bro.find_element('xpath', '/html/body/div[1]/article/div[1]/div[3]/input')

    # 找到 数据结构 的所哟开设课程
    searchTag.send_keys(courseName)

    searchBtn = bro.find_element('xpath', '/html/body/div[1]/article/div[1]/div[3]/button[1]')

    searchBtn.click()

    res_container = bro.find_element('class name', 'result-container')
    res_container.screenshot("res.png")
    course_list = bro.find_elements('class name', 'course-tr')
    # print(bro.page_source)
    # print(course_list)
    print("len of selected", len(course_list))

    cnt = 0
    for course in course_list:
        dict1 = course.get_attribute('class')
        if course.get_attribute('class').find('cv-has-selected') != -1:
            continue
        # print(dict1)
        cnt += 1
        kch = course.find_element('class name', 'cv-jxb-detail').text
        kcmc = course.find_element('class name', 'kcmc').text
        jsmc = course.find_element('class name', 'jsmc').text
        cz = course.find_element('class name', 'cv-choice')
        screenShotFileName = "./courseScreenShot/" + courseName + str(cnt) + '.png'
        course.screenshot(screenShotFileName)
        print(kch, kcmc, jsmc, "可选")
        # 尝试点击选课
        cz.click()
        # time.sleep(1)
        sureBtn = bro.find_element('class name', 'cv-sure')
        sureBtn.click()
        time.sleep(1)
        # 反馈阶段
        infoWindow = bro.find_element('class name', 'cv-body')
        # infoText = infoWindow.find_element('xpath', './')
        sureBtn = bro.find_element('class name', 'cv-sure')
        sureBtn.click()
    print("共有%d门可选择" % cnt)
    searchTag.clear()


# 初始化操作
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
}

chaojiying = Chaojiying_Client('yunzinan', 'shen66029', '937825')

bro = webdriver.Edge()

bro.implicitly_wait(10)

if not os.path.exists("./courseScreenShot"):
    os.mkdir("./courseScreenShot")

bro.get("https://xk.nju.edu.cn/")
# initialize the verification code dir
if not os.path.exists('./vc'):
    os.mkdir('./vc')
# 下载当前验证码图片
vcUrl = bro.find_element('xpath', '/html/body/div[1]/article/section/div[4]/div[1]/div[3]/img').get_attribute('src')
urllib.request.urlretrieve(vcUrl, './vc/1.jpg')
print(vcUrl)

loginNameBlank = bro.find_element('xpath', '/html/body/div[1]/article/section/div[4]/div[1]/div[1]/input')

loginNameBlank.send_keys('211850009')

loginPwdBlank = bro.find_element('xpath', '/html/body/div[1]/article/section/div[4]/div[1]/div[2]/input')

loginPwdBlank.send_keys('Jack66029shen')

'''
超级鹰获取验证码
'''
img = open('./vc/1.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
vcDict = chaojiying.PostPic(img, 1902)
vc_str = vcDict['pic_str']
print(vcDict)
#  获取输入验证码条形框
vcBlank = bro.find_element('xpath', '/html/body/div[1]/article/section/div[4]/div[1]/div[3]/input')
vcBlank.send_keys(vc_str)

time.sleep(2)

loginBtn = bro.find_element('xpath', '/html/body/div[1]/article/section/div[4]/div[1]/button')

loginBtn.click()

xkBtn = bro.find_element('id', 'courseBtn')

xkBtn.click()

time.sleep(2)

# 至此已经成功进入选课页面

zzyPageBtn = bro.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[5]/a')

zzyPageBtn.click()

chooseSelectedCourse("数据结构")
chooseSelectedCourse("计算机系统基础")


time.sleep(1000)


