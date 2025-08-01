import os
import numpy
import imageio

from business.matrix import Matrix
from business.physics import Nuclei
from business.encoding import Encoder
from business.matrixcontrol import MatrixAnalyzer

from pages.cswindow import CSWindow
from pages.filexplorer import Sleuth
from pages.fileconfig import FileEditor
from pages.workbooker import Workbooker
from pages.information import InformWindow
from pages.spectrograph import Spectrograph
from pages.locuswindows import ConfirmWindow, DeleteWindow

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent, MouseButton, KeyEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, 
    QHBoxLayout, QComboBox, QPushButton, 
    QFrame, QLabel, QFileDialog
)


class Ui_Matrixograph(object):
    def setupUi(self, dSigma):
        dSigma.setObjectName("dSigma")
        dSigma.resize(1300, 900)
        dSigma.setMinimumSize(QSize(1300, 900))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        dSigma.setFont(font)
        dSigma.setStyleSheet("QPushButton{\nbackground-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);\n}\nQPushButton:pressed{\nbackground-color: rgb(55, 55, 97);\n}")
        self.centralwidget = QWidget(dSigma)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.services_layout = QFrame(self.centralwidget)
        self.services_layout.setMinimumSize(QSize(400, 880))
        self.services_layout.setMaximumSize(QSize(800, 1760))
        self.services_layout.setFrameShape(QFrame.StyledPanel)
        self.services_layout.setFrameShadow(QFrame.Raised)
        self.services_layout.setObjectName("services_layout")
        self.verticalLayout_2 = QVBoxLayout(self.services_layout)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.angle_layout = QVBoxLayout()
        self.angle_layout.setObjectName("angle_layout")
        self.angle_info = QLabel(self.services_layout)
        self.angle_info.setMinimumSize(QSize(0, 60))
        self.angle_info.setMaximumSize(QSize(16777215, 120))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.angle_info.setFont(font)
        self.angle_info.setAlignment(Qt.AlignCenter)
        self.angle_info.setObjectName("angle_info")
        self.angle_layout.addWidget(self.angle_info)
        self.angles_box = QComboBox(self.services_layout)
        self.angles_box.setMinimumSize(QSize(0, 40))
        self.angles_box.setMaximumSize(QSize(16777215, 80))
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
        self.angles_box.setPalette(palette)
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.angles_box.setFont(font)
        self.angles_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.angles_box.setObjectName("angles_box")
        self.angle_layout.addWidget(self.angles_box)
        self.verticalLayout_2.addLayout(self.angle_layout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.bright_info = QLabel(self.services_layout)
        self.bright_info.setMinimumSize(QSize(100, 70))
        self.bright_info.setMaximumSize(QSize(100, 140))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.bright_info.setFont(font)
        self.bright_info.setObjectName("bright_info")
        self.horizontalLayout_2.addWidget(self.bright_info)
        self.bright_layout = QHBoxLayout()
        self.bright_layout.setContentsMargins(-1, 10, -1, -1)
        self.bright_layout.setObjectName("bright_layout")
        self.bright_up_button = QPushButton(self.services_layout)
        self.bright_up_button.setMinimumSize(QSize(50, 50))
        self.bright_up_button.setMaximumSize(QSize(16777215, 100))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.bright_up_button.setFont(font)
        self.bright_up_button.setObjectName("bright_up_button")
        self.bright_layout.addWidget(self.bright_up_button)
        self.bright_down_button = QPushButton(self.services_layout)
        self.bright_down_button.setMinimumSize(QSize(50, 50))
        self.bright_down_button.setMaximumSize(QSize(16777215, 100))
        self.bright_down_button.setFont(font)
        self.bright_down_button.setObjectName("bright_down_button")
        self.bright_layout.addWidget(self.bright_down_button)
        self.bright_def_button = QPushButton(self.services_layout)
        self.bright_def_button.setMinimumSize(QSize(50, 50))
        self.bright_def_button.setMaximumSize(QSize(16777215, 100))
        self.bright_def_button.setFont(font)
        self.bright_def_button.setObjectName("bright_def_button")
        self.bright_layout.addWidget(self.bright_def_button)
        self.horizontalLayout_2.addLayout(self.bright_layout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.locus_draw_button = QPushButton(self.services_layout)
        self.locus_draw_button.setMinimumSize(QSize(50, 80))
        self.locus_draw_button.setMaximumSize(QSize(16777215, 160))
        self.locus_draw_button.setFont(font)
        self.locus_draw_button.setObjectName("locus_draw_button")
        self.verticalLayout_2.addWidget(self.locus_draw_button)
        self.locus_button = QPushButton(self.services_layout)
        self.locus_button.setMinimumSize(QSize(50, 80))
        self.locus_button.setMaximumSize(QSize(16777215, 160))
        self.locus_button.setFont(font)
        self.locus_button.setObjectName("locus_button")
        self.verticalLayout_2.addWidget(self.locus_button)
        self.report_button = QPushButton(self.services_layout)
        self.report_button.setMinimumSize(QSize(50, 80))
        self.report_button.setMaximumSize(QSize(16777215, 160))
        self.report_button.setFont(font)
        self.report_button.setObjectName("report_button")
        self.verticalLayout_2.addWidget(self.report_button)
        self.spectrograph_button = QPushButton(self.services_layout)
        self.spectrograph_button.setMinimumSize(QSize(50, 80))
        self.spectrograph_button.setMaximumSize(QSize(16777215, 160))
        self.spectrograph_button.setFont(font)
        self.spectrograph_button.setObjectName("spectrograph_button")
        self.verticalLayout_2.addWidget(self.spectrograph_button)
        self.cross_section_button = QPushButton(self.services_layout)
        self.cross_section_button.setMinimumSize(QSize(50, 80))
        self.cross_section_button.setMaximumSize(QSize(16777215, 160))
        self.cross_section_button.setFont(font)
        self.cross_section_button.setObjectName("cross_section_button")
        self.verticalLayout_2.addWidget(self.cross_section_button)
        self.filedit_button = QPushButton(self.services_layout)
        self.filedit_button.setMinimumSize(QSize(50, 80))
        self.filedit_button.setMaximumSize(QSize(16777215, 160))
        self.filedit_button.setFont(font)
        self.filedit_button.setObjectName("filedit_button")
        self.verticalLayout_2.addWidget(self.filedit_button)
        self.gif_button = QPushButton(self.services_layout)
        self.gif_button.setMinimumSize(QSize(50, 80))
        self.gif_button.setMaximumSize(QSize(16777215, 160))
        self.gif_button.setFont(font)
        self.gif_button.setObjectName("gif_button")
        self.verticalLayout_2.addWidget(self.gif_button)
        self.save_button = QPushButton(self.services_layout)
        self.save_button.setMinimumSize(QSize(50, 80))
        self.save_button.setMaximumSize(QSize(16777215, 160))
        self.save_button.setFont(font)
        self.save_button.setObjectName("save_button")
        self.verticalLayout_2.addWidget(self.save_button)
        self.label = QLabel(self.services_layout)
        self.label.setMinimumSize(QSize(0, 10))
        self.label.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment( Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.horizontalLayout.addWidget(self.services_layout)
        self.matplotlib_layout = QFrame(self.centralwidget)
        self.matplotlib_layout.setMinimumSize(QSize(880, 880))
        self.matplotlib_layout.setFrameShape(QFrame.StyledPanel)
        self.matplotlib_layout.setFrameShadow(QFrame.Raised)
        self.matplotlib_layout.setObjectName("matplotlib_layout")
        self.horizontalLayout.addWidget(self.matplotlib_layout)
        dSigma.setCentralWidget(self.centralwidget)

        self.retranslateUi(dSigma)
        QMetaObject.connectSlotsByName(dSigma)

    def retranslateUi(self, dSigma):
        _translate =  QCoreApplication.translate
        dSigma.setWindowTitle(_translate("dSigma", "dSigma — E-dE matrices view"))
        self.angle_info.setText(_translate("dSigma", "Choose an angle:"))
        self.bright_info.setText(_translate("dSigma", "Brightness:"))
        self.bright_up_button.setText(_translate("dSigma", "+"))
        self.bright_down_button.setText(_translate("dSigma", "-"))
        self.bright_def_button.setText(_translate("dSigma", "Default"))
        self.locus_draw_button.setText(_translate("dSigma", "Draw Locuses Dialog"))
        self.locus_button.setText(_translate("dSigma", "Locuses On/Off"))
        self.report_button.setText(_translate("dSigma", "Workbook of experiment file"))
        self.spectrograph_button.setText(_translate("dSigma", "Open Spectres Window"))
        self.cross_section_button.setText(_translate("dSigma", "Open Cross Section Window"))
        self.filedit_button.setText(_translate("dSigma", "Experiment File Editor"))
        self.gif_button.setText(_translate("dSigma", "Make GIF"))
        self.save_button.setText(_translate("dSigma", "Save Analysis"))
        self.label.setText(_translate("dSigma", "dSigma — LLENR app for analyzing E-dE matrices."))


class DrawDialog(QWidget):
    def __init__(self, matrix: Matrix, lum: float) -> None:
        # SETUP WINDOW
        super().__init__()
        self.setWindowTitle('dSigma — Locus Draw Dialog')
        self.setWindowIcon(QIcon("./icon.ico"))
        
        self.confirmer = ConfirmWindow()
        self.deleter = DeleteWindow()

        # DATA
        self.lum = lum
        self.matrix = matrix

        self.selected_dots_x = []
        self.selected_dots_y = []

        # MATPLOTLIB INITIZIALING
        layout = QVBoxLayout(self)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.setFocusPolicy( Qt.FocusPolicy.ClickFocus)
        self.view.setFocus()
        self.view.mpl_connect('button_press_event', self.cutting)
        self.view.mpl_connect('key_press_event', self.close_locus)
        
        self.axes = self.view.figure.subplots()

        tab = QFrame(self)
        tab.setFrameShape(QFrame.StyledPanel)
        tab.setFrameShadow(QFrame.Raised)
        tab.setMaximumHeight(50)

        horizont = QHBoxLayout(tab)

        self.toolbar = NavigationToolbar2QT(self.view, tab)
        horizont.addWidget(self.toolbar)

        self.delete_button = QPushButton(tab)
        self.delete_button.setMinimumSize(100, 40)
        self.delete_button.setText('Delete Locuses')
        horizont.addWidget(self.delete_button)

        layout.addWidget(tab)
        layout.addWidget(self.view)

        self.draw_lines()

        self.delete_button.clicked.connect(self.deleter.show)
        self.confirmer.apply_button.clicked.connect(self.save_locus)
        self.deleter.apply_button.clicked.connect(self.delete_locus)

    def save_locus(self) -> None:
        nuclei = Nuclei(self.confirmer.charge_box.value(), self.confirmer.nuclon_box.value())
        points = [(self.selected_dots_x[i], self.selected_dots_y[i]) for i in range(len(self.selected_dots_x))]

        self.matrix.add_locus(nuclei, points)
        
        self.clear_selected_dots()
        self.draw_lines()

    def delete_locus(self) -> None:
        nuclei = Nuclei(self.deleter.charge_box.value(), self.deleter.nuclon_box.value())
        if nuclei not in self.matrix.locuses:
            self.window = InformWindow(f'There is no locuses in matrix of nuclei {nuclei}')
            self.window.show()
        else:
            self.matrix.locuses.pop(nuclei)
            self.draw_lines()

    def cutting(self, event: MouseEvent) -> None:
        if event.button == MouseButton.LEFT:
            self.selected_dots_x.append(int(event.xdata))
            self.selected_dots_y.append(int(event.ydata))

        if event.button == MouseButton.RIGHT and len(self.selected_dots_x) != 0:
            self.selected_dots_x.pop()
            self.selected_dots_y.pop()
            
        self.draw_lines()

    def close_locus(self, event: KeyEvent) -> None:
        if event.key == 'enter':
            self.selected_dots_x.append(self.selected_dots_x[0])
            self.selected_dots_y.append(self.selected_dots_y[0])

            self.draw_lines()

            self.confirmer.show()

    def draw_lines(self) -> None:
        self.axes.clear()
        e_de = self.matrix.numbers[:]
        e_de = e_de + 1

        locuses = self.matrix.locuses

        self.axes.pcolor(numpy.log(e_de), vmin=0, vmax=self.lum)
        self.axes.plot(self.selected_dots_x, self.selected_dots_y, color='red')
        self.axes.scatter(self.selected_dots_x, self.selected_dots_y, color='red')

        for n in locuses:
            self.axes.plot([point[0] for point in locuses[n].points], [point[1] for point in locuses[n].points], color='blue')
            self.axes.scatter([point[0] for point in locuses[n].points], [point[1] for point in locuses[n].points], color='blue')

        self.view.draw()

    def clear_selected_dots(self) -> None:
        self.selected_dots_x.clear()
        self.selected_dots_y.clear()


class Matrixograph(QMainWindow, Ui_Matrixograph):
    def __init__(self, directory: str) -> None:
        # SETUP OF WINDOW
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        self.directory = directory
        self.sleuth = Sleuth(self.directory)
        decoders = self.sleuth.all_decoders()

        # COLLECTING DATA AND PREPARE THEM TO SHOW
        self.analyzer = MatrixAnalyzer([Matrix(d) for d in decoders])
        self.__matrixes = [Matrix(d) for d in decoders]

        self.current_index = 0
        self.luminiosity = 0

        self.is_locuses_on = False

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.angles_box.currentTextChanged.connect(self.show_matrix)
        self.angles_box.addItems(map(str, self.analyzer.angles))

        # EVENT HANDLING
        self.bright_up_button.clicked.connect(self.bright_up)
        self.bright_down_button.clicked.connect(self.bright_down)
        self.bright_def_button.clicked.connect(self.bright_default)
        self.locus_draw_button.clicked.connect(self.locus_dialog)
        self.locus_button.clicked.connect(self.change_locuses_status)
        self.report_button.clicked.connect(self.open_workbook)
        self.spectrograph_button.clicked.connect(self.open_spectrograph)
        self.cross_section_button.clicked.connect(self.open_dsigma)
        self.filedit_button.clicked.connect(self.open_file_editor)
        self.gif_button.clicked.connect(self.make_gif)
        self.save_button.clicked.connect(self.save)

    def show_matrix(self) -> None:
        self.current_index = self.angles_box.currentIndex()
        self.luminiosity = self.analyzer.matrixes[self.current_index].numbers.mean() * 2
        self.draw_e_de()

    def draw_e_de(self) -> None:
        self.axes.clear()
        current = self.analyzer.matrixes[self.current_index]
        e_de = current.numbers.copy()
        e_de = e_de + 1

        self.axes.pcolor(numpy.log(e_de), vmin=0, vmax=self.luminiosity)

        if self.is_locuses_on:
            self.draw_locuses()

        self.axes.set_title(f'{current.experiment}\nLab system angle: {current.angle}')
        self.view.draw()

    def change_locuses_status(self) -> None:
        self.is_locuses_on = not self.is_locuses_on
        self.draw_e_de()

    def draw_locuses(self) -> None:
        colors = ['blue', 'red', 'green', 'yellow', 'white', 'darkred', 'purple']
        color_index = 0

        locuses = self.analyzer.matrixes[self.current_index].locuses
        for n in locuses:
            xs = [locuses[n].points[j][0] for j in range(len(locuses[n].points))]
            ys = [locuses[n].points[j][1] for j in range(len(locuses[n].points))]

            self.axes.plot(xs, ys, colors[color_index])
            color_index += 1

        self.view.draw()

    def bright_up(self) -> None:
        if self.luminiosity > 2:
            self.luminiosity -= 1
            self.draw_e_de()

    def bright_down(self) -> None:
        self.luminiosity += 1
        self.draw_e_de()

    def bright_default(self) -> None:
        self.luminiosity = self.analyzer.matrixes[self.current_index].numbers.mean() * 2
        self.draw_e_de()

    def locus_dialog(self) -> None:
        self.window = DrawDialog(self.analyzer.matrixes[self.current_index], self.luminiosity)
        self.window.show()

    def open_workbook(self) -> None:
        self.window = Workbooker(self.analyzer.matrixes[self.current_index].to_workbook())
        self.window.show()

    def open_spectrograph(self) -> None:
        self.window = Spectrograph(self.analyzer.analyzers)
        self.window.show()

    def open_dsigma(self) -> None:
        self.window = CSWindow(self.analyzer.all_dsigmas())
        self.window.show()

    def open_file_editor(self) -> None:
        self.window = FileEditor(self.analyzer.matrixes[self.current_index])
        self.window.show()

    def make_gif(self) -> None:
        if os.path.exists('Output'):
            for file in os.listdir('Output'):
                os.remove(f'Output/{file}')
        else:
            os.mkdir('Output')

        for mx in self.analyzer.matrixes:
            e_de = mx.numbers.copy()
            e_de += 1

            self.axes.pcolor(numpy.log(e_de), vmin=0, vmax=self.luminiosity)
            self.axes.set_title(f'{mx.experiment}\nLab system angle: {mx.angle}')

            self.axes.figure.savefig(f'Output/{mx.angle}.png', transparent = False,  facecolor = 'white')
            self.axes.clear()

        frames = []
        for mx in self.analyzer.matrixes:
            frames.append(imageio.v2.imread(f'Output/{mx.angle}.png'))

        name, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='GIF (*.gif)')
        while name == '':
            name, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='GIF (*.gif)')
        
        imageio.mimsave(name, frames, fps=2, loop=0)
        self.draw_e_de()

    def save(self) -> None:
        changed = self.__find_changed_ones()

        for matrix in changed:
            en = Encoder(matrix, self.directory)
            en.write_down()

        self.window = InformWindow('E-dE matrixes was saved succesfully.')
        self.window.show()

    def __find_changed_ones(self) -> None:
        found = []
        for i in range(len(self.analyzer.matrixes)):
            current = self.analyzer.matrixes[i]
            ethalon = self.__matrixes[i]

            if current.to_workbook() != ethalon.to_workbook():
                found.append(self.analyzer.matrixes[i])

        return found


if __name__ == "__main__":
    pass