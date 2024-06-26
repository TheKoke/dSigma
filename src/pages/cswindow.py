from business.physics import CrossSection

from pages.workbooker import Workbooker

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, 
    QComboBox, QHBoxLayout, QPushButton, 
    QFrame, QLabel, QFileDialog, QSpacerItem,
    QSizePolicy
)


class Ui_CSWindow(object):
    def setupUi(self, CSWindow):
        CSWindow.setObjectName("CSWindow")
        CSWindow.resize(1300, 900)
        CSWindow.setMinimumSize(QSize(1300, 900))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        CSWindow.setFont(font)
        CSWindow.setStyleSheet("QPushButton{\nbackground-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);\n}\nQPushButton:pressed{\nbackground-color: rgb(55, 55, 97);\n}")
        self.centralwidget = QWidget(CSWindow)
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
        self.reaction_label = QLabel(self.services_layout)
        self.reaction_label.setMinimumSize(QSize(42, 0))
        self.reaction_label.setMaximumSize(QSize(85, 16777215))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.reaction_label.setFont(font)
        self.reaction_label.setObjectName("reaction_label")
        self.particle_layout.addWidget(self.reaction_label)
        self.reaction_box = QComboBox(self.services_layout)
        self.reaction_box.setMinimumSize(QSize(0, 40))
        self.reaction_box.setMaximumSize(QSize(16777215, 80))
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
        self.reaction_box.setPalette(palette)
        self.reaction_box.setFont(font)
        self.reaction_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.reaction_box.setObjectName("reaction_box")
        self.particle_layout.addWidget(self.reaction_box)
        self.verticalLayout.addLayout(self.particle_layout)
        self.angle_layout = QHBoxLayout()
        self.angle_layout.setObjectName("angle_layout")
        self.state_label = QLabel(self.services_layout)
        self.state_label.setMinimumSize(QSize(42, 0))
        self.state_label.setMaximumSize(QSize(85, 16777215))
        self.state_label.setFont(font)
        self.state_label.setObjectName("state_label")
        self.angle_layout.addWidget(self.state_label)
        self.state_box = QComboBox(self.services_layout)
        self.state_box.setMinimumSize(QSize(0, 40))
        self.state_box.setMaximumSize(QSize(16777215, 80))
        self.state_box.setPalette(palette)
        self.state_box.setFont(font)
        self.state_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.state_box.setObjectName("state_box")
        self.angle_layout.addWidget(self.state_box)
        self.verticalLayout.addLayout(self.angle_layout)
        self.compare_button = QPushButton(self.services_layout)
        self.compare_button.setMinimumSize(QSize(0, 90))
        self.compare_button.setMaximumSize(QSize(16777215, 180))
        self.compare_button.setFont(font)
        self.compare_button.setObjectName("compare_button")
        self.verticalLayout.addWidget(self.compare_button)
        self.txt_button = QPushButton(self.services_layout)
        self.txt_button.setMinimumSize(QSize(0, 90))
        self.txt_button.setMaximumSize(QSize(16777215, 180))
        self.txt_button.setFont(font)
        self.txt_button.setObjectName("txt_button")
        self.verticalLayout.addWidget(self.txt_button)
        self.excel_button = QPushButton(self.services_layout)
        self.excel_button.setMinimumSize(QSize(0, 90))
        self.excel_button.setMaximumSize(QSize(16777215, 180))
        self.excel_button.setFont(font)
        self.excel_button.setObjectName("excel_button")
        self.verticalLayout.addWidget(self.excel_button)
        spacerItem = QSpacerItem(20, 420, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.workbook_button = QPushButton(self.services_layout)
        self.workbook_button.setMinimumSize(QSize(0, 90))
        self.workbook_button.setMaximumSize(QSize(16777215, 180))
        self.workbook_button.setFont(font)
        self.workbook_button.setObjectName("workbook_button")
        self.verticalLayout.addWidget(self.workbook_button)
        self.horizontalLayout.addWidget(self.services_layout)
        CSWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CSWindow)
        QMetaObject.connectSlotsByName(CSWindow)

    def retranslateUi(self, CSWindow):
        _translate = QCoreApplication.translate
        CSWindow.setWindowTitle(_translate("CSWindow", "dSigma — Cross-Section Window"))
        self.reaction_label.setText(_translate("CSWindow", "Reaction:"))
        self.state_label.setText(_translate("CSWindow", "State:"))
        self.compare_button.setText(_translate("CSWindow", "Compare All States"))
        self.txt_button.setText(_translate("CSWindow", "Save as TXT"))
        self.excel_button.setText(_translate("CSWindow", "Save as Excel File"))
        self.workbook_button.setText(_translate("CSWindow", "Open Workbook"))


class CSWindow(QMainWindow, Ui_CSWindow):
    def __init__(self, sigmas: list[CrossSection]) -> None:
        # SETUP OF WINDOW
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        # DATA
        self.sigmas = sigmas
        self.current_index = 0

        # MATPLOTLIB INITIALIZING
        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.axes = self.view.figure.subplots()
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        # EVENT HANDLING
        self.reaction_box.currentTextChanged.connect(self.take_reaction)
        self.state_box.currentTextChanged.connect(self.take_state)
        self.reaction_box.addItems([str(ds.reaction) for ds in sigmas])
        self.txt_button.clicked.connect(self.save_txt)
        self.excel_button.clicked.connect(self.save_excel)
        self.compare_button.clicked.connect(self.compare_all_states)
        self.workbook_button.clicked.connect(self.open_workbook)

    def take_reaction(self) -> None:
        index = self.reaction_box.currentIndex()
        sigma = self.sigmas[index]

        self.state_box.clear()
        self.state_box.addItems([f'{lvl} MeV' for lvl in sigma.reaction.residual_states])

    def take_state(self) -> None:
        index = self.reaction_box.currentIndex()
        sigma = self.sigmas[index]

        state = sigma.reaction.residual_states[self.state_box.currentIndex()]

        values = sigma.cm_cross_section_of(state)
        angles, xsec = values

        self.axes.clear()
        self.axes.plot(angles, xsec, color='green')
        self.axes.scatter(angles, xsec, color='green')

        self.axes.set_xlabel('Center-of-mass angle, deg.')
        self.axes.set_ylabel('Diff.cross-section, rel.units')
        self.view.draw()

    def save_txt(self) -> None:
        name, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='TXT Documents (*.txt)')
        if name == '':
            return
        
        report = self.sigmas[self.reaction_box.currentIndex()].to_workbook()

        txt = open(name, 'w')
        txt.write(report)
        txt.close()

    def save_excel(self) -> None:
        pass

    def compare_all_states(self) -> None:
        pass

    def open_workbook(self) -> None:
        self.window = Workbooker(self.sigmas[self.reaction_box.currentIndex()].to_workbook())
        self.window.show()


if __name__ == "__main__":
    pass
