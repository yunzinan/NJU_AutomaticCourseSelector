import time
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QLineEdit, QMessageBox
from crawl import Crawl
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem
from PySide2.QtCore import QTimer

# 注意 这里选择的父类 要和你UI文件窗体一样的类型
# 主窗口是 QMainWindow， 表单是 QWidget， 对话框是 QDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = QUiLoader().load('../ui/mainWindow.ui')
        self.ui.setWindowTitle("自动选课界面v0.9 Beta")
        # self.ui.setMinimumWidth(1600)
        # self.ui.setMinimumHeight(1200)
        # 初始化界面
        self.crawl = Crawl(self)
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.timerTimeOut)
        self.ui.selectBtn.clicked.connect(self.selectBtnClicked)
        self.selectZzyTimer = QTimer()
        self.selectZzyTimer.timeout.connect(self.selectZzyTimerOut)
        self.ui.paussBtn.clicked.connect(self.paussBtnClicked)
        self.ui.viewSelectedBtn.clicked.connect(self.viewMyCourse)
        self.ui.comboBox.currentIndexChanged.connect(self.viewCourse)
        self.ui.viewBtn.clicked.connect(self.showCourse)
        # self.timer.start(1000)

    # def timerTimeOut(self):
    #     self.ui.show_label.setText(self.crawl.infoDisplay)
    #     print(self.crawl.infoDisplay)
    #     print(self.ui.show_label.text())
    #     self.timer.start(1000)

    def selectBtnClicked(self):
        print("selectBtn was clicked")
        selectCourseName = self.ui.lineEdit_2.text()
        if selectCourseName == "":
            QMessageBox.warning(self.ui, "警告", "不合法的输入!")
            return
        # 获取填入的课程名称
        self.crawl.showInfo("[状态栏]已开始抢课")
        self.selectZzyTimer.start(2000)

    def paussBtnClicked(self):
        print("pauseBtn was clicked")
        self.crawl.showInfo("[状态栏]已暂停")
        self.selectZzyTimer.stop()

    def selectZzyTimerOut(self):
        print("time out! going to restart...")
        selectCourseName = self.ui.lineEdit_2.text()
        print(selectCourseName)
        # 调用select函数
        self.crawl.selectCourse(selectCourseName)
        self.selectZzyTimer.start(2000)

    def viewMyCourse(self):
        courseDetailList = self.crawl.viewMyCourse()
        courseNum = len(courseDetailList[0])  # 获取已选课程信息
        self.ui.tab_selected.setRowCount(courseNum)
        for idx in range(1, courseNum+1):
            kchItem = QTableWidgetItem(courseDetailList[0][idx-1])
            kcmcItem = QTableWidgetItem(courseDetailList[1][idx-1])
            kcjsItem = QTableWidgetItem(courseDetailList[2][idx-1])
            # self.ui.tab_selected.setItem(idx-1, 0, QTableWidgetItem(str(idx)))
            self.ui.tab_selected.setItem(idx-1, 0, kchItem)
            self.ui.tab_selected.setItem(idx-1, 1, kcmcItem)
            self.ui.tab_selected.setItem(idx-1, 2, kcjsItem)
        print("done!")

    def viewCourse(self):
        self.crawl.viewCourse(self.ui.comboBox.currentText())

    def showCourse(self):
        selectCourseName = self.ui.lineEdit_2.text()
        courseDetailList = self.crawl.viewSelectedCourse(selectCourseName)
        courseNum = len(courseDetailList[0])  # 获取已选课程信息
        self.ui.tab_show.setRowCount(courseNum)
        for idx in range(1, courseNum+1):
            kchItem = QTableWidgetItem(courseDetailList[0][idx-1])
            kcmcItem = QTableWidgetItem(courseDetailList[1][idx-1])
            kcjsItem = QTableWidgetItem(courseDetailList[2][idx-1])
            yxrsItem = QTableWidgetItem(courseDetailList[3][idx-1])
            self.ui.tab_show.setItem(idx-1, 0, kchItem)
            self.ui.tab_show.setItem(idx-1, 1, kcmcItem)
            self.ui.tab_show.setItem(idx-1, 2, kcjsItem)
            self.ui.tab_show.setItem(idx-1, 3, yxrsItem)
        print("done!")


app = QApplication([])
mainWindow = MainWindow()
mainWindow.ui.show()
app.exec_()
