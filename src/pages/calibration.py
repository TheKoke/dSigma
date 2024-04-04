from PyQt5 import QtGui
from business.analysis import Spectrum, SpectrumAnalyzer

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QColor, QKeyEvent
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QDoubleSpinBox, 
    QHBoxLayout, QPushButton, QFrame, QLabel, QWidget
)


class Ui_Calibration(object):
    def setupUi(self, Window):
        Window.setObjectName("SpectrumDemo")
        Window.resize(900, 600)
        Window.setMinimumSize(QSize(900, 600))
        Window.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        Window.setFont(font)
        Window.setStyleSheet("QPushButton{\nbackground-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);\n}\nQPushButton:pressed{\nbackground-color: rgb(55, 55,  97);\n}")
        self.centralwidget = QWidget(Window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.service_layout = QFrame(self.centralwidget)
        self.service_layout.setMinimumSize(QSize(0, 50))
        self.service_layout.setMaximumSize(QSize(16777215, 100))
        self.service_layout.setFrameShape(QFrame.StyledPanel)
        self.service_layout.setFrameShadow(QFrame.Raised)
        self.service_layout.setObjectName("service_layout")
        self.horizontalLayout = QHBoxLayout(self.service_layout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.info_label = QLabel(self.service_layout)
        self.info_label.setMinimumSize(QSize(135, 0))
        self.info_label.setMaximumSize(QSize(240, 16777215))
        font = QFont()
        font.setPointSize(11)
        self.info_label.setFont(font)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("info_label")
        self.horizontalLayout.addWidget(self.info_label)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.first_layout = QHBoxLayout()
        self.first_layout.setObjectName("first_layout")
        self.first_point = QLabel(self.service_layout)
        self.first_point.setMinimumSize(QSize(150, 0))
        self.first_point.setMaximumSize(QSize(150, 16777215))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.first_point.setFont(font)
        self.first_point.setObjectName("first_point")
        self.first_layout.addWidget(self.first_point)
        self.first_state = QDoubleSpinBox(self.service_layout)
        self.first_state.setMinimumSize(QSize(100, 0))
        self.first_state.setMaximumSize(QSize(200, 100))
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
        self.first_state.setPalette(palette)
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.first_state.setFont(font)
        self.first_state.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.first_state.setDecimals(3)
        self.first_state.setMaximum(9999999.0)
        self.first_state.setSingleStep(0.01)
        self.first_state.setObjectName("first_state")
        self.first_layout.addWidget(self.first_state)
        self.verticalLayout_2.addLayout(self.first_layout)
        self.second_layout = QHBoxLayout()
        self.second_layout.setObjectName("second_layout")
        self.second_point = QLabel(self.service_layout)
        self.second_point.setMinimumSize(QSize(150, 0))
        self.second_point.setMaximumSize(QSize(150, 16777215))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.second_point.setFont(font)
        self.second_point.setObjectName("second_point")
        self.second_layout.addWidget(self.second_point)
        self.second_state = QDoubleSpinBox(self.service_layout)
        self.second_state.setMinimumSize(QSize(100, 20))
        self.second_state.setMaximumSize(QSize(200, 100))
        self.second_state.setPalette(palette)
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.second_state.setFont(font)
        self.second_state.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.second_state.setDecimals(3)
        self.second_state.setMaximum(9999999.0)
        self.second_state.setSingleStep(0.01)
        self.second_state.setObjectName("second_state")
        self.second_layout.addWidget(self.second_state)
        self.verticalLayout_2.addLayout(self.second_layout)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.calibrate_button = QPushButton(self.service_layout)
        self.calibrate_button.setMinimumSize(QSize(110, 80))
        self.calibrate_button.setMaximumSize(QSize(500, 80))
        self.calibrate_button.setFont(font)
        self.calibrate_button.setObjectName("calibrate_button")
        self.horizontalLayout.addWidget(self.calibrate_button)
        self.output = QWidget(self.service_layout)
        self.output.setMinimumSize(QSize(100, 0))
        self.output.setMaximumSize(QSize(200, 16777215))
        self.output.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.output.setObjectName("output")
        self.horizontalLayout_2 = QHBoxLayout(self.output)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.output_label = QLabel(self.output)
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.output_label.setFont(font)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setObjectName("output_label")
        self.horizontalLayout_2.addWidget(self.output_label)
        self.horizontalLayout.addWidget(self.output)
        self.verticalLayout.addWidget(self.service_layout)
        self.matplotlib_layout = QFrame(self.centralwidget)
        self.matplotlib_layout.setFrameShape(QFrame.StyledPanel)
        self.matplotlib_layout.setFrameShadow(QFrame.Raised)
        self.matplotlib_layout.setObjectName("matplotlib_layout")
        self.verticalLayout.addWidget(self.matplotlib_layout)
        Window.setCentralWidget(self.centralwidget)

        self.retranslateUi(Window)
        QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, SpectrumDemo):
        _translate = QCoreApplication.translate
        SpectrumDemo.setWindowTitle(_translate("SpectrumDemo", "dSigma — Calibration Window"))
        self.info_label.setText(_translate("SpectrumDemo", "Pick the points on spectrum and select states of residual nuclei, then press enter or \"Calibrate\" button"))
        self.first_point.setText(_translate("SpectrumDemo", "First point"))
        self.first_state.setSuffix(_translate("SpectrumDemo", " MeV"))
        self.second_point.setText(_translate("SpectrumDemo", "Second point"))
        self.second_state.setSuffix(_translate("SpectrumDemo", " MeV"))
        self.calibrate_button.setText(_translate("SpectrumDemo", "Calibrate"))
        self.output_label.setText(_translate("SpectrumDemo", "Calibration equation"))


class CalibrationWindow(QMainWindow, Ui_Calibration):
    def __init__(self, analyzer: SpectrumAnalyzer, index: int) -> None:
        # WINDOW SETUP
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        # DATA
        self.analyzer = analyzer
        self.index = index

        self.selected_dots_x = []
        self.selected_dots_y = []

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.setFocusPolicy( Qt.FocusPolicy.ClickFocus)
        self.view.setFocus()
        self.view.mpl_connect('button_press_event', self.pick)
        
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.calibrate_button.clicked.connect(self.apply)
        self.draw()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.EnterKeyType:
            self.apply()

        return super().keyPressEvent(a0)

    def pick(self, event: MouseEvent) -> None:
        if event.button == MouseButton.LEFT:
            self.selected_dots_x.append(int(round(event.xdata)))
            self.selected_dots_y.append(int(round(event.ydata)))

        if event.button == MouseButton.RIGHT and len(self.selected_dots_x) != 0:
            self.selected_dots_x.pop()
            self.selected_dots_y.pop()

        self.show_picked()

    def show_picked(self) -> None:
        if len(self.selected_dots_x) < 2:
            return

        first_point = (self.selected_dots_x[-2], self.selected_dots_y[-2])
        second_point = (self.selected_dots_x[-1], self.selected_dots_y[-1])

        self.first_point.setText(f'{first_point[0]}; {first_point[1]}')
        self.second_point.setText(f'{second_point[0]}; {second_point[1]}')

        self.draw()

    def apply(self) -> None:
        if len(self.selected_dots_x) < 2:
            return

        first_dot = self.selected_dots_x[-2]
        second_dot = self.selected_dots_x[-1]

        first_state = self.first_state.value()
        second_state = self.second_state.value()

        self.analyzer.calibrate(self.index, (first_dot, second_dot), (first_state, second_state))

        shift = self.analyzer.spectrums[self.index].scale_shift
        channel_value = self.analyzer.spectrums[self.index].scale_value
        self.output_label.setText(f"E(ch) = {round(channel_value, 3)} + {round(shift, 3)}")

    def draw(self) -> None:
        spectrum = self.analyzer.spectrums[self.index]

        self.axes.clear()
        for i in range(len(spectrum.data)):
            self.axes.plot([i + 1, i + 1], [0, spectrum.data[i]], color='blue')

        if len(self.selected_dots_x) >= 2:
            dots = [spectrum.data[self.selected_dots_x[-2] - 1], spectrum.data[self.selected_dots_x[-1] - 1]]
            self.axes.scatter(self.selected_dots_x[-2:], dots, color='red')

        self.axes.plot(list(range(1, len(spectrum.data) + 1)), spectrum.data, color='blue')
        self.view.draw()


if __name__ == '__main__':
    pass
