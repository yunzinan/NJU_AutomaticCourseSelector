import os.path
import time
import urllib.request

from selenium import webdriver

from chaojiying import Chaojiying_Client


class Crawl:

    def __init__(self, _parent):
        self.studentInfo = {
            'name': '211850000',  # 你的学号
            'pwd': '123456' # 你的选课网站密码
        }
        self.driver = webdriver.Edge()
        self.infoDisplay = "[状态栏]"
        self.parent = _parent
        # 初始化headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
        }
        # 初始化截屏文件夹
        if not os.path.exists("../courseScreenShot"):
            os.mkdir("../courseScreenShot")

        self.login()

    def showInfo(self, _info):
        # self.infoDisplay = _info
        self.parent.ui.show_label.setText(_info)
    def login(self):
        # 登录选课平台
        # 初始化超级鹰
        chaojiying = Chaojiying_Client('zhangsan', 'yourpwd', 'yourID')  # 具体请查看超级鹰的API
        self.driver.implicitly_wait(10)
        self.driver.get("https://xk.nju.edu.cn/")
        # 初始化验证码文件夹
        if not os.path.exists('../vc'):
            os.mkdir('../vc')
        # 下载当前验证码图片
        vcUrl = self.driver.find_element('xpath',
                                         '/html/body/div[1]/article/section/div[4]/div[1]/div[3]/img').get_attribute(
            'src')
        print("验证码URL:", vcUrl)
        urllib.request.urlretrieve(vcUrl, '../vc/1.jpg')

        loginNameBlank = self.driver.find_element('xpath',
                                                  '/html/body/div[1]/article/section/div[4]/div[1]/div[1]/input')

        loginNameBlank.send_keys(self.studentInfo['name'])

        loginPwdBlank = self.driver.find_element('xpath',
                                                 '/html/body/div[1]/article/section/div[4]/div[1]/div[2]/input')

        loginPwdBlank.send_keys(self.studentInfo['pwd'])

        # 超级鹰获取验证码
        img = open('../vc/1.jpg', 'rb').read()

        vcDict = chaojiying.PostPic(img, 1902)
        vc_str = vcDict['pic_str']
        print(vcDict)
        #  获取输入验证码条形框
        vcBlank = self.driver.find_element('xpath', '/html/body/div[1]/article/section/div[4]/div[1]/div[3]/input')
        vcBlank.send_keys(vc_str)
        # 至此完成了三个框的输入

        loginBtn = self.driver.find_element('xpath', '/html/body/div[1]/article/section/div[4]/div[1]/button')
        loginBtn.click()  # 点击一次"登录按钮"

        '''
        注: 新加入了一个"选课身份"的按钮以及确认按钮
        '''
        selectBtn = self.driver.find_element('xpath',
                                             '/html/body/div[4]/div[2]/div[1]/div/div/table/tbody/tr[1]/td[1]/div/input')
        selectBtn.click()
        confirmBtn = self.driver.find_element('xpath', '/html/body/div[4]/div[2]/div[2]/button[2]')
        confirmBtn.click()
        time.sleep(1)
        xkBtn = self.driver.find_element('id', 'courseBtn')
        xkBtn.click()  # 点击"进入选课"按钮
        time.sleep(2)  # 停顿两秒

    def selectCourse(self, courseName):
        time.sleep(2)

        searchTag = self.driver.find_element('xpath', '/html/body/div[1]/article/div[1]/div[3]/input')
        # 找到 courseName 的所有开设课程
        searchTag.send_keys(courseName)

        searchBtn = self.driver.find_element('xpath', '/html/body/div[1]/article/div[1]/div[3]/button[1]')

        searchBtn.click()  # 点击搜索
        time.sleep(1)

        # res_container = self.driver.find_element('class name', 'result-container')
        # res_container.screenshot("res.png")
        course_list = self.driver.find_elements('class name', 'course-tr')
        # print(self.driver.page_source)
        # print(course_list)
        if len(course_list) == 0:
            self.showInfo("[状态栏]没有搜索到任何课程")
            searchTag.clear()
            return
        self.showInfo("len of selected:" + str(len(course_list)))
        cnt = 0
        for course in course_list:
            dict1 = course.get_attribute('class')
            if course.get_attribute('class').find('cv-has-selected') != -1:
                self.showInfo("[状态栏]没有可选按钮, 跳过该课程")
                time.sleep(2)
                continue

            td_cz = course.find_element('xpath', './td[8]')
            tr_cz = td_cz.find_element('xpath', './a[2]')
            if tr_cz.get_attribute('class').find('cv-has-selected') != -1:  # 已选, 不可选
                self.showInfo("[状态栏]课程已选, 跳过该课程")
                time.sleep(2)
                continue
            elif tr_cz.get_attribute('class').find('cv-disabled') != -1:  # 已满, 不可选
                self.showInfo("[状态栏]课程已满, 跳过该课程")
                time.sleep(2)
                continue
            # print(dict1)
            cnt += 1
            kch = course.find_element('class name', 'cv-jxb-detail').text
            kcmc = course.find_element('class name', 'kcmc').text
            jsmc = course.find_element('class name', 'jsmc').text
            # cz = course.find_element('class name', 'cv-choice')
            # screenShotFileName = "../courseScreenShot/" + courseName + str(cnt) + '.png'
            # course.screenshot(screenShotFileName)
            self.showInfo("[状态栏]" + kch + kcmc + jsmc + "可选")
            # 尝试点击选课
            tr_cz.click()
            # time.sleep(1)
            sureBtn = self.driver.find_element('class name', 'cv-sure')
            sureBtn.click()
            time.sleep(1)
            # 反馈阶段
            infoWindow = self.driver.find_element('class name', 'cv-body')
            infoText = infoWindow.find_element('xpath', './div').text
            self.showInfo("[状态栏]" + infoText)
            print("[状态栏]" + infoText)
            time.sleep(1)
            sureBtn = self.driver.find_element('class name', 'cv-sure')
            sureBtn.click()
            time.sleep(2)
        # self.showInfo("共有%d门可选择" % cnt)

        searchTag.clear()
        return
    '''
    查看我已选的课程
    '''
    def viewMyCourse(self):

        zyBtn = self.driver.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[1]/a')

        zyBtn.click() # 切换到已选课程界面

        selectedCourseBtn = self.driver.find_element('xpath', '/html/body/div[1]/article/div[1]/div[3]/button[2]')

        selectedCourseBtn.click()

        wdckBtn = self.driver.find_element('class name', 'jqx-tabs-titleContentWrapper')

        wdckBtn.click()
        time.sleep(1)

        # courseBody = self.driver.find_element('class name', 'course-body')

        selectedCourseList = self.driver.find_elements('xpath',
                                                       '/html/body/div[3]/div[2]/div[1]/div/div/div[2]/div[1]/table/tbody/tr')

        print("len:", len(selectedCourseList))

        kchList = []
        kcmcList = []
        kcjsList = []

        for idx in range(len(selectedCourseList)):
            i = idx + 1
            coursePath = '/html/body/div[3]/div[2]/div[1]/div/div/div[2]/div[1]/table/tbody/tr' + '[' + str(i) + ']'
            course = self.driver.find_element('xpath', coursePath)
            print(coursePath)
            kch = course.find_element('class name', 'kch').text
            kcmc = course.find_element('class name', 'kcmc').text
            kcjs = course.find_element('class name', 'jsmc').text
            kchList.append(kch)
            kcmcList.append(kcmc)
            kcjsList.append(kcjs)
        courseDetailList = [kchList, kcmcList, kcjsList]
        closeBtn = self.driver.find_element('xpath', '/html/body/div[3]/div[2]/div[2]/button')
        closeBtn.click()
        return courseDetailList
    '''
    查看任意课程
    '''
    def viewCourse(self, colName):
        if colName == "跨专业":
            zzyBtn = self.driver.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[3]/a')
            zzyBtn.click()
            time.sleep(1)
        elif colName == "收藏":
            scBtn = self.driver.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[5]/a')
            scBtn.click()
            time.sleep(1)
        # elif colName == "专业":
        #     zybtn = self.driver.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[1]/a')
        #     zybtn.click()
        #     time.sleep(1)
        elif colName == "通修":
            txBtn = self.driver.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[4]/a')
            txBtn.click()
            time.sleep(1)
        elif colName == "公共-导学/研讨/通识":
            ggBtn = self.driver.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[2]/a')
            ggBtn.click()
            time.sleep(1)
            dytBtn = self.driver.find_element('xpath', '/html/body/div[1]/article/div[1]/div[4]/div[1]')
            dytBtn.click()
            time.sleep(1)
        elif colName == "公共-公选课":
            ggBtn = self.driver.find_element('xpath', '/html/body/div[1]/header/div[2]/ul/li[2]/a')
            ggBtn.click()
            time.sleep(1)
            gxkBtn = self.driver.find_element('xpath', '/html/body/div[1]/article/div[1]/div[4]/div[2]')
            gxkBtn.click()
            time.sleep(1)

    '''
    查看已选课程
    负责将搜索到的课程信息显示在界面上
    '''
    def viewSelectedCourse(self, courseName):
        searchTag = self.driver.find_element('xpath', '/html/body/div[1]/article/div[1]/div[3]/input')
        # 找到 courseName 的所有开设课程
        searchTag.send_keys(courseName)

        searchBtn = self.driver.find_element('xpath', '/html/body/div[1]/article/div[1]/div[3]/button[1]')

        searchBtn.click()  # 点击搜索
        time.sleep(1)

        res_container = self.driver.find_element('class name', 'result-container')
        # res_container.screenshot("res.png")
        course_list = self.driver.find_elements('class name', 'course-tr')
        # print(self.driver.page_source)
        # print(course_list)
        if len(course_list) == 0:
            self.showInfo("[状态栏]没有搜索到任何课程")
            kchList = []
            kcmcList = []
            kcjsList = []
            yxrslist = []
            courseDetailList = [kchList, kcmcList, kcjsList, yxrslist]
            searchTag.clear()
            return courseDetailList
        print("len of selected", len(course_list))
        cnt = 0
        kchList = []
        kcmcList = []
        kcjsList = []
        yxrslist = []

        for course in course_list:
            dict1 = course.get_attribute('class')
            if course.get_attribute('class').find('cv-has-selected') != -1:
                continue
            # print(dict1)
            cnt += 1
            kch = course.find_element('class name', 'cv-jxb-detail').text
            kcmc = course.find_element('class name', 'kcmc').text
            jsmc = course.find_element('class name', 'jsmc').text
            yxrs = course.find_element('class name', 'yxrs').text
            kchList.append(kch)
            kcmcList.append(kcmc)
            kcjsList.append(jsmc)
            yxrslist.append(yxrs)
        courseDetailList = [kchList, kcmcList, kcjsList, yxrslist]
        searchTag.clear()
        self.showInfo("[状态栏]注意:不显示已经选中的课程")
        return courseDetailList




