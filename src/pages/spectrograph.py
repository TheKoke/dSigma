import numpy

from business.analysis import SpectrumAnalyzer

from pages.workbooker import Workbooker
from pages.gaussograph import Gaussograph
from pages.calibration import CalibrationWindow

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, 
    QComboBox, QHBoxLayout, QPushButton, 
    QFrame, QLabel, QFileDialog
)


class Ui_Spectrograph(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 900)
        MainWindow.setMinimumSize(QSize(1300, 900))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QPushButton{\nbackground-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);\n}\nQPushButton:pressed{\nbackground-color: rgb(55, 55, 97);\n}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.matplotlib_layout = QFrame(self.centralwidget)
        self.matplotlib_layout.setMinimumSize(QSize(880, 880))
        self.matplotlib_layout.setMaximumSize(QSize(2000, 1760))
        self.matplotlib_layout.setFrameShape(QFrame.StyledPanel)
        self.matplotlib_layout.setFrameShadow(QFrame.Raised)
        self.matplotlib_layout.setObjectName("matplorlib_layout")
        self.horizontalLayout.addWidget(self.matplotlib_layout)
        self.services_layout = QFrame(self.centralwidget)
        self.services_layout.setMinimumSize(QSize(400, 880))
        self.services_layout.setMaximumSize(QSize(800, 1760))
        self.services_layout.setFrameShape(QFrame.StyledPanel)
        self.services_layout.setFrameShadow(QFrame.Raised)
        self.services_layout.setObjectName("services_layout")
        self.verticalLayout = QVBoxLayout(self.services_layout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.particle_layout = QHBoxLayout()
        self.particle_layout.setObjectName("particle_layout")
        self.particle_label = QLabel(self.services_layout)
        self.particle_label.setMinimumSize(QSize(42, 0))
        self.particle_label.setMaximumSize(QSize(85, 16777215))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.particle_label.setFont(font)
        self.particle_label.setObjectName("particle_label")
        self.particle_layout.addWidget(self.particle_label)
        self.particle_box = QComboBox(self.services_layout)
        self.particle_box.setMinimumSize(QSize(0, 30))
        self.particle_box.setMaximumSize(QSize(16777215, 45))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        brush = QBrush(QColor(85, 85, 127))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        brush = QBrush(QColor(0, 120, 215))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush)
        self.particle_box.setPalette(palette)
        self.particle_box.setFont(font)
        self.particle_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.particle_box.setObjectName("particle_box")
        self.particle_layout.addWidget(self.particle_box)
        self.verticalLayout.addLayout(self.particle_layout)
        self.angle_layout = QHBoxLayout()
        self.angle_layout.setObjectName("angle_layout")
        self.angle_label = QLabel(self.services_layout)
        self.angle_label.setMinimumSize(QSize(42, 0))
        self.angle_label.setMaximumSize(QSize(85, 16777215))
        self.angle_label.setFont(font)
        self.angle_label.setObjectName("angle_label")
        self.angle_layout.addWidget(self.angle_label)
        self.angle_box = QComboBox(self.services_layout)
        self.angle_box.setMinimumSize(QSize(0, 30))
        self.angle_box.setMaximumSize(QSize(16777215, 45))
        self.angle_box.setPalette(palette)
        self.angle_box.setFont(font)
        self.angle_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.angle_box.setObjectName("angle_box")
        self.angle_layout.addWidget(self.angle_box)
        self.verticalLayout.addLayout(self.angle_layout)
        self.gaussian_button = QPushButton(self.services_layout)
        self.gaussian_button.setMinimumSize(QSize(0, 90))
        self.gaussian_button.setMaximumSize(QSize(16777215, 180))
        self.gaussian_button.setFont(font)
        self.gaussian_button.setObjectName("gaussian_button")
        self.verticalLayout.addWidget(self.gaussian_button)
        self.calibrate_button = QPushButton(self.services_layout)
        self.calibrate_button.setMinimumSize(QSize(0, 90))
        self.calibrate_button.setMaximumSize(QSize(16777215, 180))
        self.calibrate_button.setFont(font)
        self.calibrate_button.setObjectName("calibrate_button")
        self.verticalLayout.addWidget(self.calibrate_button)
        self.peaks_button = QPushButton(self.services_layout)
        self.peaks_button.setMinimumSize(QSize(0, 90))
        self.peaks_button.setMaximumSize(QSize(16777215, 180))
        self.peaks_button.setFont(font)
        self.peaks_button.setObjectName("peaks_button")
        self.verticalLayout.addWidget(self.peaks_button)
        self.impurity_button = QPushButton(self.services_layout)
        self.impurity_button.setMinimumSize(QSize(0, 90))
        self.impurity_button.setMaximumSize(QSize(16777215, 180))
        self.impurity_button.setFont(font)
        self.impurity_button.setObjectName("impurity_button")
        self.verticalLayout.addWidget(self.impurity_button)
        self.workbook_button = QPushButton(self.services_layout)
        self.workbook_button.setMinimumSize(QSize(0, 90))
        self.workbook_button.setMaximumSize(QSize(16777215, 180))
        self.workbook_button.setFont(font)
        self.workbook_button.setObjectName("workbook_button")
        self.verticalLayout.addWidget(self.workbook_button)
        self.ladder_button = QPushButton(self.services_layout)
        self.ladder_button.setMinimumSize(QSize(0, 90))
        self.ladder_button.setMaximumSize(QSize(16777215, 180))
        self.ladder_button.setFont(font)
        self.ladder_button.setObjectName("ladder_button")
        self.verticalLayout.addWidget(self.ladder_button)
        self.save_button = QPushButton(self.services_layout)
        self.save_button.setMinimumSize(QSize(0, 90))
        self.save_button.setMaximumSize(QSize(16777215, 180))
        self.save_button.setFont(font)
        self.save_button.setObjectName("save_button")
        self.verticalLayout.addWidget(self.save_button)
        self.horizontalLayout.addWidget(self.services_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "dSigma — Spectra Window"))
        self.particle_label.setText(_translate("MainWindow", "Particle:"))
        self.angle_label.setText(_translate("MainWindow", "Angle:"))
        self.gaussian_button.setText(_translate("MainWindow", "Approximate by Gaussian"))
        self.calibrate_button.setText(_translate("MainWindow", "Calibrate"))
        self.peaks_button.setText(_translate("MainWindow", "Show Peaks"))
        self.impurity_button.setText(_translate("MainWindow", "Validate Impurities"))
        self.workbook_button.setText(_translate("MainWindow", "Open Workbook"))
        self.ladder_button.setText(_translate("MainWindow", "Build Ladder View"))
        self.save_button.setText(_translate("MainWindow", "Save as .txt"))


class Ui_LadderViewer(object):
    def setupUi(self, LadderViewer):
        LadderViewer.setObjectName("LadderViewer")
        LadderViewer.resize(800, 600)
        LadderViewer.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(LadderViewer)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mpl_layout = QFrame(self.centralwidget)
        self.mpl_layout.setFrameShape(QFrame.StyledPanel)
        self.mpl_layout.setFrameShadow(QFrame.Raised)
        self.mpl_layout.setObjectName("mpl_layout")
        self.horizontalLayout.addWidget(self.mpl_layout)
        LadderViewer.setCentralWidget(self.centralwidget)

        self.retranslateUi(LadderViewer)
        QMetaObject.connectSlotsByName(LadderViewer)

    def retranslateUi(self, LadderViewer):
        _translate = QCoreApplication.translate
        LadderViewer.setWindowTitle(_translate("LadderViewer", "dSigma — Ladder/Kinematics viewer"))


class LadderViewer(QMainWindow, Ui_LadderViewer):
    def __init__(self, spectra: SpectrumAnalyzer) -> None:
        # SETUP OF WINDOW
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        # DATA
        self.spectra = spectra
        self.picked = -1

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.mpl_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.mpl_connect('button_press_event', self.add_picked)

        self.axes = self.view.figure.subplots()

        tab = QFrame(self.mpl_layout)
        tab.setFrameShape(QFrame.StyledPanel)
        tab.setFrameShadow(QFrame.Raised)
        tab.setMaximumHeight(50)

        horizont = QHBoxLayout(tab)

        self.toolbar = NavigationToolbar2QT(self.view, tab)
        horizont.addWidget(self.toolbar)

        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setWeight(75)
        self.picked_angle = QLabel('Pointer on angle=', tab)
        self.picked_angle.setMinimumSize(100, 50)
        self.picked_angle.setFont(font)
        self.picked_angle.setAlignment(Qt.AlignmentFlag.AlignTop)
        horizont.addWidget(self.picked_angle)

        layout.addWidget(tab)
        layout.addWidget(self.view)

        self.draw()

    def add_picked(self, event: MouseEvent) -> None:
        if event.button == MouseButton.LEFT and event.dblclick:
            allrange = self.spectra.spectrums[:]
            mean = sum([sp.data.mean() for sp in allrange]) / len(allrange)

            angle = event.ydata / mean

            self.picked = numpy.abs(numpy.array([sp.angle for sp in self.spectra.spectrums]) - angle).argmin()
            self.picked_angle.setText(f'Pointer on angle={self.spectra.spectrums[self.picked].angle}')
            self.draw()

    def draw(self) -> None:
        allrange = self.spectra.spectrums[:]
        mean = sum([sp.data.mean() for sp in allrange]) / len(allrange)

        self.axes.clear()
        for i in range(len(allrange)):
            channels = list(range(1, len(allrange[i].data) + 1))
            offseted = allrange[i].data + allrange[i].angle * mean

            if i == self.picked:
                self.axes.plot(channels, offseted, color='red')
                continue

            self.axes.plot(channels, offseted, color='blue')

        self.view.draw()


class Spectrograph(QMainWindow, Ui_Spectrograph):
    def __init__(self, analitics: list[SpectrumAnalyzer]) -> None:
        # WINDOW SETUP
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        # DATA
        self.analitics = analitics
        self.current_index = 0
        
        self.pointers = []

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.mpl_connect('button_press_event', self.add_pointer)
        self.axes = self.view.figure.subplots()

        tab = QFrame(self.matplotlib_layout)
        tab.setFrameShape(QFrame.StyledPanel)
        tab.setFrameShadow(QFrame.Raised)
        tab.setMaximumHeight(50)

        horizont = QHBoxLayout(tab)

        self.toolbar = NavigationToolbar2QT(self.view, tab)
        horizont.addWidget(self.toolbar)

        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.linear_sum = QLabel('SUM=', tab)
        self.linear_sum.setMinimumSize(100, 30)
        self.linear_sum.setFont(font)
        horizont.addWidget(self.linear_sum)

        layout.addWidget(tab)
        layout.addWidget(self.view)

        # EVENT HANDLING
        self.angle_box.currentTextChanged.connect(self.draw_angle)
        self.angle_box.currentTextChanged.connect(self.pointers.clear)
        self.particle_box.currentTextChanged.connect(self.take_current)
        particles = [analyzer.spectrums[0].reaction.fragment for analyzer in self.analitics]
        self.particle_box.addItems([str(p) for p in particles])

        self.gaussian_button.clicked.connect(self.open_gaussograph)
        self.calibrate_button.clicked.connect(self.open_calibration)
        self.peaks_button.clicked.connect(self.show_peaks)
        self.impurity_button.clicked.connect(self.validate_impurities)
        self.workbook_button.clicked.connect(self.open_workbook)
        self.ladder_button.clicked.connect(self.build_ladder)
        self.save_button.clicked.connect(self.save)

    def add_pointer(self, event: MouseEvent) -> None:
        if event.button == MouseButton.LEFT and event.dblclick:
            if len(self.pointers) < 2:
                self.pointers.append(int(event.xdata))
            else:
                self.pointers.pop(0)
                self.pointers.append(int(event.xdata))

            self.draw_pointers()

    def draw_pointers(self) -> None:
        angle = float(self.angle_box.currentText())
        analitics = self.analitics[self.current_index]
        maximum = analitics.spectrum_of_angle(angle).data.max()
        
        self.draw_angle()
        for i in range(len(self.pointers)):
            self.axes.plot([self.pointers[i], self.pointers[i]], [0, maximum], color='red')
        
        self.show_linear_sum()
        self.view.draw()

    def show_linear_sum(self) -> None:
        if len(self.pointers) < 2:
            return

        angle = float(self.angle_box.currentText())
        analitics = self.analitics[self.current_index]

        first = self.pointers[0]
        second = self.pointers[1]

        channels_sum = analitics.spectrum_of_angle(angle).data[min(first, second): max(first, second)].sum()
        self.linear_sum.setText(f'SUM={channels_sum}')

    def open_gaussograph(self) -> None:
        if len(self.pointers) < 2:
            return
        
        angle = float(self.angle_box.currentText())
        analitics = self.analitics[self.current_index]

        self.window = Gaussograph(analitics.spectrum_of_angle(angle), self.pointers)
        self.window.show()

    def open_calibration(self) -> None:
        angle = float(self.angle_box.currentText())
        analitics = self.analitics[self.current_index]

        self.window = CalibrationWindow(analitics, angle)
        self.window.show()

    def show_peaks(self) -> None:
        angle = float(self.angle_box.currentText())
        spectrum = self.analitics[self.current_index].spectrum_of_angle(angle)

        if spectrum.is_calibrated and len(spectrum.peaks) == 0:
            self.analitics[self.current_index].approximate(angle)

        self.draw_angle()

    def validate_impurities(self) -> None:
        pass

    def open_workbook(self) -> None:
        angle = float(self.angle_box.currentText())
        spectrum = self.analitics[self.current_index].spectrum_of_angle(angle)

        self.window = Workbooker(spectrum.to_workbook())
        self.window.show()

    def build_ladder(self) -> None:
        self.window = LadderViewer(self.analitics[self.current_index])
        self.window.show()

    def save(self) -> None:
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='TXT Documents (*.txt)')
        if name == '':
            return
        
        angle = float(self.angle_box.currentText())
        analitics = self.analitics[self.current_index]
        spectrum = analitics.spectrum_of_angle(angle).data

        txt = open(name, 'w')
        for i in range(len(spectrum)):
            print(f'{i + 1}\t{spectrum[i]}', file=txt)

        txt.close()

    def take_current(self) -> None:
        self.current_index = int(self.particle_box.currentIndex())
        angles = [spectrum.angle for spectrum in self.analitics[self.current_index].spectrums]

        self.linear_sum.setText('SUM=')
        self.angle_box.clear()
        self.angle_box.addItems(map(str, sorted(angles)))

    def draw_angle(self) -> None:
        if self.angle_box.currentText() == '':
            return

        angle = float(self.angle_box.currentText())
        spectrum = self.analitics[self.current_index].spectrum_of_angle(angle)

        self.axes.clear()
        
        for i in range(len(spectrum.data)):
            self.axes.plot([i + 1, i + 1], [0, spectrum.data[i]], color='blue')

        for peak in spectrum.peaks.values():
            self.axes.plot(peak.three_sigma(), peak.function(), color='red')
        
        self.axes.plot(list(range(1, len(spectrum.data) + 1)), spectrum.data, color='blue')
        self.view.draw()


if __name__ == '__main__':
    pass
