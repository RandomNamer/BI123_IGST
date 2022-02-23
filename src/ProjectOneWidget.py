from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from util import *
import time


class ProjectOneTabWidget(QFrame):
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

        # 添加功能
        self.label_1 = QLabel()
        self.label_1.setText("Histogram and Threshold")
        self.label_1.setEnabled(True)
        self.label_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_1.setFixedHeight(50)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)

        self.label_2 = QLabel()
        self.label_2.setText("Manual Thresholding")
        self.label_2.setEnabled(True)
        self.label_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.label_2.setFixedHeight(30)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)

        self.threshSliderIndicator = QLabel()
        self.threshSliderIndicator.setText("Current Value:")
        self.threshSlider = QSlider()
        self.threshSlider.setOrientation(Qt.Horizontal)
        self.threshSlider.setMinimum(0)
        self.threshSlider.setMaximum(255)

        self.threshSliderValueLayout = QHBoxLayout()
        self.label_3 = QLabel(self.labelList)
        self.label_3.setText("0")
        self.label_4 = QLabel(self.labelList)
        self.label_4.setText("255")
        self.label_4.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.threshSliderValueLayout.addWidget(self.label_3)
        self.threshSliderValueLayout.addWidget(self.label_4)

        self.label_5 = QLabel()
        self.label_5.setAlignment(Qt.AlignCenter)
        self.label_5.setFont(font)
        self.label_5.setText("Auto Thresholding")

        self.radio_1 = QRadioButton()
        self.radio_1.setText("Otsu")

        self.radio_2 = QRadioButton()
        self.radio_2.setText("Entropy")
        s = QSlider()
        s.setMinimum(0)
        s.setMaximum(10)
        s.setTickInterval(1)
        s.setOrientation(Qt.Horizontal)
        self.entropySlider = s
        self.entropySliderIndicator = QLabel()
        self.entropySliderIndicator.setText("Entropy Segmentation Level:")
        self.entropySliderValueLayout = QHBoxLayout()
        self.entropySliderMin = QLabel(self.labelList)
        self.entropySliderMin.setText("0.0")
        self.entropySliderMax = QLabel(self.labelList)
        self.entropySliderMax.setText("1.0")
        self.entropySliderMax.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.entropySliderValueLayout.addWidget(self.entropySliderMin)
        self.entropySliderValueLayout.addWidget(self.entropySliderMax)



        self.button = QPushButton()
        self.button.setStyleSheet("margin: auto 12px; padding: 4px; background-color:rgb(200,200,255);")
        self.button.setText("Calculate")

        self.label_6 = QLabel()
        self.label_6.setText("Current Threshold:")
        font = QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)

        self.vSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # 收敛功能
        self.labelListLayout.addWidget(self.label_1, alignment=Qt.AlignHCenter |  Qt.AlignTop)
        self.labelListLayout.addWidget(self.label_2, alignment=Qt.AlignHCenter |  Qt.AlignTop)
        self.labelListLayout.addWidget(self.threshSliderIndicator)
        self.labelListLayout.addWidget(self.threshSlider)
        self.labelListLayout.addLayout(self.threshSliderValueLayout)
        self.labelListLayout.addWidget(self.label_5)
        self.labelListLayout.addWidget(self.radio_1)
        self.labelListLayout.addWidget(self.radio_2)
        self.labelListLayout.addWidget(self.entropySliderIndicator)
        self.labelListLayout.addWidget(self.entropySlider)
        self.labelListLayout.addLayout(self.entropySliderValueLayout)
        self.labelListLayout.addWidget(self.button)
        self.labelListLayout.addWidget(self.label_6)
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

        self.threshImg = QLabel()
        self.threshImg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageGridLayout.addWidget(self.threshImg, 1, 0, 1, 1)

        self.entropyImg = QLabel()
        self.entropyImg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageGridLayout.addWidget(self.entropyImg, 1, 1, 1, 1)

        # 信号处理
        updateImgSignal.connect(self.updateOriginImgHandler)
        self.button.clicked.connect(self.calSignalHandler)
        self.threshSlider.valueChanged.connect(self.threshSliderValueChangedHandler)

        # States:
        self.imageArrayReady = False
        self.histogramReady = False
        self.manualThresholdReady = False
        self.otsuThreshReady = False

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
        else:
            self.imageArray = readFromJpgAndNormalize(filePath);
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
        self.entropyImg.setPixmap(emptyQtPixelMap(self.entropyImg.size()))
        # self.histImg.setPixmap(pixmap_resized)
        self.threshImg.setPixmap(emptyQtPixelMap(self.threshImg.size()))

    def calSignalHandler(self):
        # value = self.threshSlider.value()
        if not self.imageArrayReady:
            QMessageBox.information(self, "Info", "Select an imag to get started", QMessageBox.Ok)
            return
        if self.otsuThreshReady:
            print("Otsu already calculated for this image")
        isOtsu = self.radio_1.isChecked()
        isEntropy = self.radio_2.isChecked()
        begin = time.time()
        print(" Otsu / Entropy")
        if isOtsu:
            threshvalue = otsuThresh(self.imageArray)
            otsuimg = np_to_qt(normalizeBinary(point(self.imageArray, threshvalue)))
            pix = QPixmap.fromImage(otsuimg)
            pixmap_resized = pix.scaled(self.entropyImg.size(), Qt.KeepAspectRatio)
            self.entropyImg.setPixmap(pixmap_resized)

            self.label_6.setText("Current Otsu Value:" + " " + str(threshvalue))
            print("Processed Otsu in", time.time() - begin)
            self.otsuThreshReady = True
        elif isEntropy:
            level = self.entropySlider.value() / 10
            seg = entropyLevelSeg(self.imageArray, level)
            img = np_to_qt(seg)
            pix = QPixmap.fromImage(img)
            pixmap_resized = pix.scaled(self.entropyImg.size(), Qt.KeepAspectRatio)
            self.entropyImg.setPixmap(pixmap_resized)

            self.label_6.setText("Current Entropy level: " + str(level))
            print("Processed Entropy in", time.time() - begin)

    def threshSliderValueChangedHandler(self):
        value = self.threshSlider.value()
        self.threshSliderIndicator.setText("Current Value: " + str(value))
        if not self.imageArrayReady:
            QMessageBox.information(self, "Info", "Select an imag to get started", QMessageBox.Ok)
            return
        start = time.time()
        threshImg = normalizeBinary(point(self.imageArray, value))
        threshImg = np_to_qt(threshImg)
        pix = QPixmap.fromImage(threshImg)
        pixmap_resized = pix.scaled(self.threshImg.size(), Qt.KeepAspectRatio)
        self.threshImg.setPixmap(pixmap_resized)
        print("Global Thresholding, value ", value, ", in ", (time.time() - start), "s")

