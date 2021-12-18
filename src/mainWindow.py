import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ProjectWidget import ProjectWidegt

openFromDir = "/Users/zzy/Desktop/Image Processing CourseWorks/"


class MainWindow(QMainWindow):

    updateImgSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.resize(1340,1000)

        self.mCentralWidget = QWidget()
        self.setCentralWidget(self.mCentralWidget)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.mCentralWidget.setLayout(self.mainLayout)

        self.tabWidget = QTabWidget(self.mCentralWidget)
        self.tabWidget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        #菜单栏部分
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, self.width(), 30))
        self.menuBar.setObjectName("menubar")
        self.menu = QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.actionOpen = QAction(self)
        self.actionOpen.setObjectName("actionopen_study")
        self.setMenuBar(self.menuBar)
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionOpen)
        self.menuBar.addAction(self.menu.menuAction())

        self.mainLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.tabWidget)

        self.project1 = ProjectWidegt(self.updateImgSignal)
        self.tabWidget.addTab(self.project1, "")

        self.project2 = ProjectWidegt(self.updateImgSignal)
        self.tabWidget.addTab(self.project2, "")

        self.project3 = ProjectWidegt(self.updateImgSignal)
        self.tabWidget.addTab(self.project3, "")

        self.project4 = ProjectWidegt(self.updateImgSignal)
        self.tabWidget.addTab(self.project4, "")


        #信号绑定
        self.actionOpen.triggered.connect(self.openFileHandler)

        self.retranslateUi(self)

        self.show()

    def openFileHandler(self):
        imgPath, ftype = QFileDialog.getOpenFileName(self, "Open File", openFromDir, "*.dcm")
        # imgPath = r'E:/Image Processing CourseWorks/Image Processing CourseWorks/lab1/1091.dcm'

        if os.path.isdir(imgPath): return

        print(imgPath)
        self.updateImgSignal.emit(imgPath)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open Image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project1), _translate("MainWindow", "Project 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project2), _translate("MainWindow", "Project 2"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project3), _translate("MainWindow", "Project 3"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.project4), _translate("MainWindow", "Project 4"))