import os
import sys

from PyQt5.QtWidgets import *

from pages.welcome import WelcomeWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = WelcomeWindow()

    wind.show()
    app.exec()
