import sys

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5.QtWidgets import *

class Spectrograph(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        #WINDOW SETTINGS 
        self.setFixedSize(1200, 900)
        self.setWindowTitle('Spectrum')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Spectrograph()
    wind.show()
    app.exec()