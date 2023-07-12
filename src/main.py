import os
import sys
import typing
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from matplotlib.figure import Figure
from matplotlib.patches import PathPatch
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from pages.welcome import Ui_Welcome
from pages.matrixograph import Ui_Demo
from pages.spectrograph import Ui_SpectrumDemo

from business.matrix import Demo
from business.parsing import USBParser
from business.analysis import Analyzer, Spectrum
from business.electronics import Telescope, Detector


class ExperimentConfig:
    def __init__(self) -> None:
        pass

    def get_electronics(self) -> Telescope:
        pass

    def gather_detector(self) -> Detector:
        pass


class Sleuth:
    def __init__(self, main_directory: str) -> None:
        self.main = main_directory

    def all_parsers(self) -> list[USBParser]:
        files = self.sort()
        return [USBParser(file) for file in files]

    def sort(self) -> list[str]:
        directories = os.listdir(self.main)
        return self.only_usb(directories)
    
    def only_usb(self, dirs: list[str]) -> list[str]:
        sifted = self.only_files(dirs)
        return [self.main + '/' + file for file in sifted if '.usb' in file]
    
    def only_files(self, dirs: list[str]) -> list[str]:
        return [direc for direc in dirs if '.' if direc]


class WelcomeWindow(QDialog, Ui_Welcome):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.path = ''

        self.file_button.clicked.connect(self.take_directory)
        self.enter_button.clicked.connect(self.start)

    def take_directory(self) -> None:
        paths = QFileDialog.getExistingDirectory(self)
        self.input.setText(paths)
        self.path = paths

    def start(self) -> None:
        if self.path == '':
            return

        self.window = RevWindow(self.path)
        self.window.show()
        self.hide()


class SpectrumRevWindow(QMainWindow, Ui_SpectrumDemo):
    def __init__(self) -> None:
        # SETUP OF WINDOW
        super().__init__()
        self.setupUi(self)

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)


class RevWindow(QMainWindow, Ui_Demo):
    def __init__(self, directory: str) -> None:
        # SETUP OF WINDOW
        super().__init__()
        self.setupUi(self)

        # COLLECTING DATA AND PREPARING TO SHOW
        self.usbs = Sleuth(directory).sort()
        self.demo: Demo = None
        self.matrix = None
        self.luminiosity = 0

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.angles_box.currentTextChanged.connect(self.open_usb)
        self.angles_box.addItems(self.usbs)

        # EVENT HANDLING
        self.show_button.clicked.connect(self.draw_matrix)
        self.bright_up_button.clicked.connect(self.bright_up)
        self.bright_down_button.clicked.connect(self.bright_down)
        self.bright_def_button.clicked.connect(self.bright_default)
        self.locus_show_button.clicked.connect(self.draw_locuses)
        self.locus_unshow_button.clicked.connect(self.undraw_locuses)
        self.spectrum_button.clicked.connect(self.open_spectrums)
        self.report_button.clicked.connect(self.open_workbook)

    def open_usb(self) -> None:
        parser = USBParser(self.angles_box.currentText())
        self.demo = Demo(parser)
        self.matrix = self.demo.matrix()
        self.luminiosity = self.matrix.mean() * 2

    def open_workbook(self) -> None:
        pass

    def bright_up(self) -> None:
        if self.luminiosity > 20:
            self.luminiosity -= 10
            self.draw_matrix()

    def bright_down(self) -> None:
        self.luminiosity += 10
        self.draw_matrix()

    def bright_default(self) -> None:
        self.luminiosity = self.matrix.mean() * 2
        self.draw_matrix()

    def draw_locuses(self) -> None:
        locuses = self.demo.locuses()
        for locus in locuses:
            self.axes.plot([locus[i][0] for i in range(len(locus))], [locus[i][1] for i in range(len(locus))])

        self.view.draw()

    def undraw_locuses(self) -> None:
        self.axes.clear()
        self.draw_matrix()
        self.view.draw()

    def open_spectrums(self) -> None:
        locuses = self.demo.locuses()
        for locus in locuses:
            self.demo.locus_spectrum(locus)

    def draw_matrix(self) -> None:
        self.axes.clear()
        self.axes.pcolor(self.matrix, vmin=-self.luminiosity / 2, vmax=self.luminiosity / 2, cmap='bone_r')
        self.view.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = WelcomeWindow()

    wind.show()
    app.exec()
