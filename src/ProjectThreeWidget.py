from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from util import *
import time


class ProjectThreeTabWidget(QFrame):
    calSignal = pyqtSignal()
    filePath = ""

    def __init__(self, updateImgSignal, ParentWidget=None):
        QFrame.__init__(self, ParentWidget)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Plain)

        self.hLayout = QHBoxLayout()
        self.hLayout.setSpacing(5)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hLayout)

        # 功能区
        self.labelList = QFrame(self)
        self.hLayout.addWidget(self.labelList)
        self.labelList.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.labelList.setFixedWidth(340)
        self.labelList.setFrameShape(QFrame.StyledPanel)
        self.labelList.setFrameShadow(QFrame.Plain)

        self.labelListLayout = QVBoxLayout()
        self.labelListLayout.setContentsMargins(5, 5, 5, 5)
        self.labelListLayout.setSpacing(10)
        self.labelList.setLayout(self.labelListLayout)


        label = QLabel()
        label.setText("Basic Morphological Operations")
        label.setEnabled(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label.setFixedHeight(50)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.title = label

        s = QSlider()
        s.setMinimum(3)
        s.setMaximum(11)
        s.setTickInterval(2)
        s.setOrientation(Qt.Horizontal)
        self.kernelSizeSlider = s
        self.kernelSizeSliderIndicator = QLabel()
        self.kernelSizeSliderIndicator.setText("Kernel Size:")
        self.kernelSizeSliderValueLayout = QHBoxLayout()
        self.kernelSizeSliderMin = QLabel(self.labelList)
        self.kernelSizeSliderMin.setText("3")
        self.kernelSizeSliderMax = QLabel(self.labelList)
        self.kernelSizeSliderMax.setText("11")
        self.kernelSizeSliderMax.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.kernelSizeSliderValueLayout.addWidget(self.kernelSizeSliderMin)
        self.kernelSizeSliderValueLayout.addWidget(self.kernelSizeSliderMax)

        label = QLabel()
        label.setText("Dilation and Erosion")
        label.setEnabled(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label.setFixedHeight(30)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.de_label = label

        self.dilation = QRadioButton()
        self.dilation.setText("Dilation")
        self.erosion = QRadioButton()
        self.erosion.setText("Erosion")


        #self.NR
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setFont(font)
        label.setText("Opening and Closing")
        self.oc_label = label

        self.opening = QRadioButton()
        self.opening.setText("Open")
        self.closing = QRadioButton()
        self.closing.setText("Close")

        self.button = QPushButton()
        self.button.setStyleSheet("margin: auto 12px; padding: 4px; background-color:rgb(200,200,255)")
        self.button.setText("Calculate")

        self.vSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 收敛功能
        self.labelListLayout.addWidget(self.title)
        self.labelListLayout.addWidget(self.kernelSizeSliderIndicator)
        self.labelListLayout.addWidget(self.kernelSizeSlider)
        self.labelListLayout.addLayout(self.kernelSizeSliderValueLayout)
        self.labelListLayout.addWidget(self.de_label)
        self.labelListLayout.addWidget(self.dilation)
        self.labelListLayout.addWidget(self.erosion)
        self.labelListLayout.addWidget(self.oc_label)
        self.labelListLayout.addWidget(self.opening)
        self.labelListLayout.addWidget(self.closing)
        self.labelListLayout.addWidget(self.button)
        self.labelListLayout.addItem(self.vSpacer)

        # 图像区
        self.imageGrid = QFrame(self)
        self.hLayout.addWidget(self.imageGrid)
        self.imageGrid.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageGrid.setFrameShape(QFrame.StyledPanel)
        self.imageGrid.setFrameShadow(QFrame.Plain)

        self.imageGridLayout = QGridLayout()
        self.imageGridLayout.setSpacing(5)
        self.imageGridLayout.setContentsMargins(10, 10, 10, 10)
        self.imageGridLayout.setAlignment(Qt.AlignCenter)
        self.imageGrid.setLayout(self.imageGridLayout)

        self.originImg = QLabel()
        self.originImg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageGridLayout.addWidget(self.originImg, 0, 0, 1, 1)

        self.histImg = QLabel()
        self.histImg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageGridLayout.addWidget(self.histImg, 0, 1, 1, 1)

        self.operation1Img = QLabel()
        self.operation1Img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageGridLayout.addWidget(self.operation1Img, 1, 0, 1, 1)

        self.operation2Img = QLabel()
        self.operation2Img.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageGridLayout.addWidget(self.operation2Img, 1, 1, 1, 1)

        # 信号处理
        updateImgSignal.connect(self.updateOriginImgHandler)
        self.button.clicked.connect(self.calSignalHandler)
        self.kernelSizeSlider.valueChanged.connect(
            lambda: self.kernelSizeSliderIndicator.setText("Kernel Size: " + str(self.kernelSizeSlider.value())))

        # States:
        self.imageArrayReady = False
        self.histogramReady = False

    def updateOriginImgHandler(self, filePath):
        print(self.imageGrid.size())
        print(self.originImg.size())
        if filePath == self.filePath: return
        self.filePath = filePath
        self.otsuThreshReady = False
        self.manualThresholdReady = False
        self.imageArrayReady = False
        self.histogramReady = False
        if filePath.endswith("dcm"):
            self.imageArray = readFromDicomAndNormalize(filePath);
        else: self.imageArray = readFromJpgAndNormalize(filePath);
        self.imageArrayReady = True
        qim = np_to_qt(self.imageArray)
        pix = QPixmap.fromImage(qim)
        pixmap_resized = pix.scaled(self.originImg.size(), Qt.KeepAspectRatio)
        self.originImg.setPixmap(pixmap_resized)
        begin = time.time()
        pix = histControlImg(self.imageArray)
        pixmap_resized = pix.scaled(self.histImg.size())
        self.histImg.setPixmap(pixmap_resized)
        print("Generated histogram in", time.time() - begin, "s")
        self.histogramReady = True
        self.operation2Img.setPixmap(emptyQtPixelMap(self.operation2Img.size()))
        # self.histImg.setPixmap(pixmap_resized)
        self.operation1Img.setPixmap(emptyQtPixelMap(self.operation1Img.size()))

    def calSignalHandler(self):
        # value = self.threshSlider.value()
        if not self.imageArrayReady:
            QMessageBox.information(self, "Info", "Select an imag to get started", QMessageBox.Ok)
            return
        e = self.erosion.isChecked()
        d = self.dilation.isChecked()
        o = self.opening.isChecked()
        c = self.closing.isChecked()

        kernelSize = self.kernelSizeSlider.value()
        begin = time.time()
        print(" Calculate 2 morph operations")
        if e:
            setImageArrayForWidget(erosion(self.imageArray, ksize=kernelSize), self.operation1Img)
            print("Processed Erosion in", time.time() - begin, "s")
        elif d:
            setImageArrayForWidget(dilation(self.imageArray, ksize=kernelSize), self.operation1Img)
            print("Processed Dilation in", time.time() - begin, "s")
        begin = time.time()
        if o:
            setImageArrayForWidget(opening(self.imageArray, ksize=kernelSize), self.operation2Img)
            print("Processed Opening in", time.time() - begin, "s")
        elif c:
            setImageArrayForWidget(closing(self.imageArray, ksize=kernelSize), self.operation2Img)
            print("Processed Closing in", time.time() - begin, "s")