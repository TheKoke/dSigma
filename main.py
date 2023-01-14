from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import matplotlib.pyplot as plt
import sys

def default_window() -> None:
    app = QApplication(sys.argv)
    wind = QMainWindow()

    wind.setGeometry(200, 200, 600, 800)

    wind.show()
    app.exec_()

if __name__ == 'main':
    default_window()