import sys

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5.QtWidgets import *

from src.matrix import Matrix

class Matrixograph(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Matrixograph()
    wind.show()
    app.exec()