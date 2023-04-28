import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5.QtWidgets import *

class WorkBooker(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        #WINDOW SETTINGS 
        self.setFixedSize(1200, 900)
        self.setWindowTitle('Workbook')

if __name__ == '__main__':
    app = QApplication()
    wind = WorkBooker()
    wind.show()
    app.exec()