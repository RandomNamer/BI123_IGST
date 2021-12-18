import sys

from PyQt5.QtWidgets import QApplication

from mainWindow import MainWindow

# D:\python\envs\MRViewer\Lib\site-packages\PyQt5\Qt5\plugins
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

