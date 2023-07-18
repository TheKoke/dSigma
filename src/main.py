import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from pages.welcome import Ui_Welcome
from pages.matrixograph import Ui_MatrixDemo
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
        return sorted(self.only_usb(directories))
    
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
    def __init__(self, spectres: list[list[int]]) -> None:
        # SETUP OF WINDOW
        super().__init__()
        self.setupUi(self)

        self.spectrums = spectres

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.calibrate_button.setEnabled(False)
        self.peaks_button.setEnabled(False)

        # EVENT HANDLING
        self.particle_box.currentIndexChanged.connect(self.draw_spectrum)
        self.txt_button.clicked.connect(self.save_spectrum)

        self.draw_spectrum()

    def draw_spectrum(self) -> None:
        index = self.particle_box.currentIndex()
        spectrum = self.spectrums[index]

        self.axes.clear()
        self.axes.plot(list(range(1, len(spectrum) + 1)), spectrum)
        self.view.draw()

    def save_spectrum(self) -> None:
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='TXT Documents (*.txt)')
        if name == '':
            return
        
        index = self.particle_box.currentIndex()
        spectrum = self.spectrums[index]

        txt = open(name, 'w')
        for i in range(len(spectrum)):
            print(f'{i + 1}\t{spectrum[i]}', file=txt)

        txt.close()


class View(QMainWindow):
    def __init__(self, report: str):
        super().__init__()
        self.resize(800, 600)
        self.setMinimumSize(800, 600)

        self.setWindowTitle("dSigma — Workbook viewer")

        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)

        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setPlainText(report)
        self.plainTextEdit.setReadOnly(True)
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.setCentralWidget(self.centralwidget)


class RevWindow(QMainWindow, Ui_MatrixDemo):
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
        self.start_button.setEnabled(False)

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
        self.matrix = self.demo.numbers
        self.luminiosity = self.matrix.mean() * 2

    def open_workbook(self) -> None:
        if self.demo is None:
            return

        self.window = View(self.demo.to_workbook())
        self.window.show()

    def bright_up(self) -> None:
        if self.demo is None:
            return
        
        if self.luminiosity > 20:
            self.luminiosity -= 10
            self.draw_matrix()

    def bright_down(self) -> None:
        if self.demo is None:
            return
        
        self.luminiosity += 10
        self.draw_matrix()

    def bright_default(self) -> None:
        if self.demo is None:
            return
        
        self.luminiosity = self.matrix.mean() * 2
        self.draw_matrix()

    def draw_locuses(self) -> None:
        colors = ['blue', 'red', 'green', 'yellow', 'white']
        locuses = self.demo.locuses()
        for i in range(len(locuses)):
            xs = [locuses[i][j][0] for j in range(len(locuses[i]))]
            ys = [locuses[i][j][1] for j in range(len(locuses[i]))]

            self.axes.plot(xs, ys, colors[i])

        self.view.draw()

    def undraw_locuses(self) -> None:
        if self.demo is None:
            return
        
        self.axes.clear()
        self.draw_matrix()
        self.view.draw()

    def open_spectrums(self) -> None:
        if self.demo is None:
            return
        
        locuses = self.demo.locuses()
        spectres = []
        for locus in locuses:
            spectres.append(self.demo.locus_spectrum(locus))

        self.window = SpectrumRevWindow(spectres)
        self.window.show()

    def draw_matrix(self) -> None:
        if self.demo is None:
            return
        
        self.axes.clear()
        self.axes.pcolor(self.matrix, vmin=-self.luminiosity / 2, vmax=self.luminiosity / 2, cmap='bone_r')
        self.view.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = WelcomeWindow()

    wind.show()
    app.exec()
