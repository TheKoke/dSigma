from business.yard import NucleiConverter
from business.analysis import SpectrumAnalyzer

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, 
    QComboBox, QHBoxLayout, QPushButton, 
    QFrame, QLabel
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
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
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
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.angle_label.setFont(font)
        self.angle_label.setObjectName("angle_label")
        self.angle_layout.addWidget(self.angle_label)
        self.angle_box = QComboBox(self.services_layout)
        self.angle_box.setMinimumSize(QSize(0, 30))
        self.angle_box.setMaximumSize(QSize(16777215, 45))
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
        self.angle_box.setPalette(palette)
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.angle_box.setFont(font)
        self.angle_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.angle_box.setObjectName("angle_box")
        self.angle_layout.addWidget(self.angle_box)
        self.verticalLayout.addLayout(self.angle_layout)
        self.calibrate_button = QPushButton(self.services_layout)
        self.calibrate_button.setMinimumSize(QSize(0, 90))
        self.calibrate_button.setMaximumSize(QSize(16777215, 180))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.calibrate_button.setFont(font)
        self.calibrate_button.setObjectName("calibrate_button")
        self.verticalLayout.addWidget(self.calibrate_button)
        self.peaks_button = QPushButton(self.services_layout)
        self.peaks_button.setMinimumSize(QSize(0, 90))
        self.peaks_button.setMaximumSize(QSize(16777215, 180))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.peaks_button.setFont(font)
        self.peaks_button.setObjectName("peaks_button")
        self.verticalLayout.addWidget(self.peaks_button)
        self.impurity_button = QPushButton(self.services_layout)
        self.impurity_button.setMinimumSize(QSize(0, 90))
        self.impurity_button.setMaximumSize(QSize(16777215, 180))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.impurity_button.setFont(font)
        self.impurity_button.setObjectName("impurity_button")
        self.verticalLayout.addWidget(self.impurity_button)
        self.workbook_button = QPushButton(self.services_layout)
        self.workbook_button.setMinimumSize(QSize(0, 90))
        self.workbook_button.setMaximumSize(QSize(16777215, 180))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.workbook_button.setFont(font)
        self.workbook_button.setObjectName("workbook_button")
        self.verticalLayout.addWidget(self.workbook_button)
        self.save_button = QPushButton(self.services_layout)
        self.save_button.setMinimumSize(QSize(0, 90))
        self.save_button.setMaximumSize(QSize(16777215, 180))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.save_button.setFont(font)
        self.save_button.setObjectName("save_button")
        self.verticalLayout.addWidget(self.save_button)
        self.ladder_button = QPushButton(self.services_layout)
        self.ladder_button.setMinimumSize(QSize(0, 90))
        self.ladder_button.setMaximumSize(QSize(16777215, 180))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ladder_button.setFont(font)
        self.ladder_button.setObjectName("ladder_button")
        self.verticalLayout.addWidget(self.ladder_button)
        self.horizontalLayout.addWidget(self.services_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "dSigma — Spectra Window"))
        self.particle_label.setText(_translate("MainWindow", "Particle:"))
        self.angle_label.setText(_translate("MainWindow", "Angle:"))
        self.calibrate_button.setText(_translate("MainWindow", "Calibrate"))
        self.peaks_button.setText(_translate("MainWindow", "Show Peaks"))
        self.impurity_button.setText(_translate("MainWindow", "Validate Impurities"))
        self.workbook_button.setText(_translate("MainWindow", "Open Workbook"))
        self.save_button.setText(_translate("MainWindow", "Save Spectrum Analysis"))
        self.ladder_button.setText(_translate("MainWindow", "Build Ladder View"))


class Spectrograph(QMainWindow, Ui_Spectrograph):
    def __init__(self, analitics: list[SpectrumAnalyzer]) -> None:
        # WINDOW SETUP
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        self.analitics = analitics
        self.current_index = 0

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.angle_box.currentTextChanged.connect(self.draw_angle)
        self.particle_box.currentTextChanged.connect(self.take_current)
        particles = [analyzer.spectrums[0].reaction.fragment for analyzer in self.analitics]
        self.particle_box.addItems([NucleiConverter.to_string(p) for p in particles])

        self.ladder_button.clicked.connect(self.build_ladder)

    def take_current(self) -> None:
        self.current_index = int(self.particle_box.currentIndex())
        angles = [spectrum.angle for spectrum in self.analitics[self.current_index].spectrums]

        self.angle_box.clear()
        self.angle_box.addItems([str(a) for a in angles])

    def draw_angle(self) -> None:
        angle_index = self.angle_box.currentIndex()
        spectrum = self.analitics[self.current_index].spectrums[angle_index]

        self.axes.clear()
        
        for i in range(len(spectrum.data)):
            self.axes.plot([i + 1, i + 1], [0, spectrum.data[i]], color='blue')
        
        self.axes.plot(list(range(1, len(spectrum.data) + 1)), spectrum.data, color='blue')
        self.view.draw()

    # TODO: Fix this method.
    def build_ladder(self) -> None:
        spectra = self.analitics[self.current_index].spectrums[:]
        spectra = sorted(spectra, key=lambda x: x.angle)

        self.axes.clear()
        for i in range(len(spectra)):
            self.axes.plot(list(range(1, len(spectra[i].data) + 1)), spectra[i].data + i * 5000, color='blue')

        self.view.draw()


if __name__ == '__main__':
    pass
