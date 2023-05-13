import sys

from PyQt5.QtWidgets import *
from pages import *
from controllers import *


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        #WINDOW SETTINGS 
        self.setFixedSize(1200, 900)
        self.setWindowTitle('PySpectrum')

        #TAB INITIALIZING
        self.tabs = QTabWidget(self)
        self.tabs.setEnabled(True)
        self.tabs.setGeometry(0, 0, 1000, 900)

        #BUTTONS INITIALIZING
        file_btn = QPushButton('Open a file', self)
        file_btn.setGeometry(1010, 10, 180, 90)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()

    wind.show()
    app.exec()
