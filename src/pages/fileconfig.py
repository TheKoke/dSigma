from business.matrix import Matrix
from business.physics import Nuclei

from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QVBoxLayout, 
    QComboBox, QHBoxLayout, QLineEdit, 
    QFrame, QLabel, QSpacerItem, QSizePolicy,
    QDoubleSpinBox, QPushButton
)


BEAM_INFO = 'Beam  ---------------------------------------'
TARGET_INFO = 'Target --------------------------------------------'
ENERGY_INFO = 'Beam Energy ----------------------------------------------'
ANGLE_INFO = 'Laboratory Angle ---------------------------------'
THICKNESS_INFO = 'Thickness:'
RESOLUTION_INFO = 'Resolution:'
DISTANCE_INFO = 'Beam span base ---------------------------------'
RADIUS_INFO = 'Collimator radius ---------------------------------'
INTEGRATOR_INFO = 'Integrator counts ---------------------------------'
MISSCALC_INFO = 'Misscalculation ---------------------------------'
INTCONST_INFO = 'Integrator constant ---------------------------------'
OKAY_INFO = 'Correct 👍'
NOT_OKAY_INFO = 'ERROR!👎'


class Ui_FileConfigWindow(object):
    def setupUi(self, FileConfigWindow):
        FileConfigWindow.setObjectName("FileConfigWindow")
        FileConfigWindow.resize(800, 800)
        FileConfigWindow.setMinimumSize(QSize(800, 800))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        FileConfigWindow.setFont(font)
        FileConfigWindow.setStyleSheet("QPushButton{background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);font: 63 12pt \"Bahnschrift SemiBold\";}QPushButton:pressed{background-color: rgb(55, 55, 97);}")
        self.centralwidget = QWidget(FileConfigWindow)
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.main_layout = QFrame(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_layout.sizePolicy().hasHeightForWidth())
        self.main_layout.setSizePolicy(sizePolicy)
        self.main_layout.setMinimumSize(QSize(600, 750))
        self.main_layout.setMaximumSize(QSize(1500, 16777215))
        self.main_layout.setStyleSheet("font: 63 14pt \"Bahnschrift SemiBold\";")
        self.main_layout.setFrameShape(QFrame.StyledPanel)
        self.main_layout.setFrameShadow(QFrame.Raised)
        self.main_layout.setObjectName("main_layout")
        self.verticalLayout = QVBoxLayout(self.main_layout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.beam_layout = QHBoxLayout()
        self.beam_layout.setObjectName("beam_layout")
        self.beam_label = QLabel(self.main_layout)
        self.beam_label.setMinimumSize(QSize(370, 30))
        self.beam_label.setMaximumSize(QSize(370, 80))
        self.beam_label.setObjectName("beam_label")
        self.beam_layout.addWidget(self.beam_label)
        self.beam_line = QLineEdit(self.main_layout)
        self.beam_line.setMinimumSize(QSize(50, 40))
        self.beam_line.setMaximumSize(QSize(16777215, 80))
        self.beam_line.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.beam_line.setAlignment(Qt.AlignCenter)
        self.beam_line.setObjectName("beam_line")
        self.beam_layout.addWidget(self.beam_line)
        self.beam_correct_label = QLabel(self.main_layout)
        self.beam_correct_label.setMaximumSize(QSize(120, 80))
        self.beam_correct_label.setObjectName("beam_correct_label")
        self.beam_layout.addWidget(self.beam_correct_label)
        self.verticalLayout.addLayout(self.beam_layout)
        self.target_layout = QHBoxLayout()
        self.target_layout.setObjectName("target_layout")
        self.target_label = QLabel(self.main_layout)
        self.target_label.setMinimumSize(QSize(370, 0))
        self.target_label.setMaximumSize(QSize(370, 80))
        self.target_label.setObjectName("target_label")
        self.target_layout.addWidget(self.target_label)
        self.target_line = QLineEdit(self.main_layout)
        self.target_line.setMinimumSize(QSize(50, 40))
        self.target_line.setMaximumSize(QSize(16777215, 80))
        self.target_line.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.target_line.setAlignment(Qt.AlignCenter)
        self.target_line.setObjectName("target_line")
        self.target_layout.addWidget(self.target_line)
        self.target_correct_label = QLabel(self.main_layout)
        self.target_correct_label.setMaximumSize(QSize(120, 80))
        self.target_correct_label.setObjectName("target_correct_label")
        self.target_layout.addWidget(self.target_correct_label)
        self.verticalLayout.addLayout(self.target_layout)
        self.energy_layout = QHBoxLayout()
        self.energy_layout.setObjectName("energy_layout")
        self.energy_label = QLabel(self.main_layout)
        self.energy_label.setMinimumSize(QSize(370, 0))
        self.energy_label.setMaximumSize(QSize(370, 80))
        self.energy_label.setObjectName("energy_label")
        self.energy_layout.addWidget(self.energy_label)
        self.energy_box = QDoubleSpinBox(self.main_layout)
        self.energy_box.setMinimumSize(QSize(170, 40))
        self.energy_box.setMaximumSize(QSize(16777215, 80))
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
        self.energy_box.setPalette(palette)
        self.energy_box.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.energy_box.setAlignment(Qt.AlignCenter)
        self.energy_box.setDecimals(3)
        self.energy_box.setMaximum(999999.0)
        self.energy_box.setSingleStep(0.1)
        self.energy_box.setObjectName("energy_box")
        self.energy_layout.addWidget(self.energy_box)
        self.verticalLayout.addLayout(self.energy_layout)
        self.angle_layout = QHBoxLayout()
        self.angle_layout.setObjectName("angle_layout")
        self.angle_label = QLabel(self.main_layout)
        self.angle_label.setMinimumSize(QSize(370, 0))
        self.angle_label.setMaximumSize(QSize(370, 80))
        self.angle_label.setObjectName("angle_label")
        self.angle_layout.addWidget(self.angle_label)
        self.angle_box = QDoubleSpinBox(self.main_layout)
        self.angle_box.setMinimumSize(QSize(180, 40))
        self.angle_box.setMaximumSize(QSize(16777215, 80))
        self.angle_box.setPalette(palette)
        self.angle_box.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.angle_box.setAlignment(Qt.AlignCenter)
        self.angle_box.setMaximum(999999.0)
        self.angle_box.setSingleStep(0.1)
        self.angle_box.setObjectName("angle_box")
        self.angle_layout.addWidget(self.angle_box)
        self.angle_correct_label = QLabel(self.main_layout)
        self.angle_correct_label.setMaximumSize(QSize(120, 80))
        self.angle_correct_label.setObjectName("angle_correct_label")
        self.angle_layout.addWidget(self.angle_correct_label)
        self.verticalLayout.addLayout(self.angle_layout)
        self.telescope_layout = QVBoxLayout()
        self.telescope_layout.setObjectName("telescope_layout")
        self.telescope_info = QLabel(self.main_layout)
        self.telescope_info.setMinimumSize(QSize(0, 30))
        self.telescope_info.setMaximumSize(QSize(16777215, 60))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.telescope_info.setFont(font)
        self.telescope_info.setAlignment(Qt.AlignCenter)
        self.telescope_info.setObjectName("telescope_info")
        self.telescope_layout.addWidget(self.telescope_info)
        self.detector_layout = QHBoxLayout()
        self.detector_layout.setObjectName("detector_layout")
        self.de_layout = QVBoxLayout()
        self.de_layout.setObjectName("de_layout")
        self.de_detector_info = QLabel(self.main_layout)
        self.de_detector_info.setMinimumSize(QSize(0, 30))
        self.de_detector_info.setMaximumSize(QSize(16777215, 60))
        self.de_detector_info.setFont(font)
        self.de_detector_info.setAlignment(Qt.AlignCenter)
        self.de_detector_info.setObjectName("de_detector_info")
        self.de_layout.addWidget(self.de_detector_info)
        self.de_element_box = QComboBox(self.main_layout)
        self.de_element_box.setMinimumSize(QSize(0, 40))
        self.de_element_box.setMaximumSize(QSize(16777215, 60))
        self.de_element_box.setPalette(palette)
        self.de_element_box.setFont(font)
        self.de_element_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.de_element_box.setObjectName("de_element_box")
        self.de_element_box.addItem("")
        self.de_element_box.addItem("")
        self.de_element_box.addItem("")
        self.de_layout.addWidget(self.de_element_box)
        self.de_thickness_layout = QHBoxLayout()
        self.de_thickness_layout.setObjectName("de_thickness_layout")
        self.de_thick_info = QLabel(self.main_layout)
        self.de_thick_info.setMinimumSize(QSize(130, 50))
        self.de_thick_info.setMaximumSize(QSize(260, 80))
        self.de_thick_info.setFont(font)
        self.de_thick_info.setObjectName("de_thick_info")
        self.de_thickness_layout.addWidget(self.de_thick_info)
        self.de_thickness_box = QDoubleSpinBox(self.main_layout)
        self.de_thickness_box.setMinimumSize(QSize(100, 40))
        self.de_thickness_box.setMaximumSize(QSize(200, 80))
        self.de_thickness_box.setFont(font)
        self.de_thickness_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.de_thickness_box.setAlignment(Qt.AlignCenter)
        self.de_thickness_box.setMaximum(999999999.99)
        self.de_thickness_box.setProperty("value", 50.0)
        self.de_thickness_box.setPalette(palette)
        self.de_thickness_box.setObjectName("de_thickness_box")
        self.de_thickness_layout.addWidget(self.de_thickness_box)
        self.de_layout.addLayout(self.de_thickness_layout)
        self.de_resolution_layout = QHBoxLayout()
        self.de_resolution_layout.setObjectName("de_resolution_layout")
        self.de_res_info = QLabel(self.main_layout)
        self.de_res_info.setMinimumSize(QSize(130, 50))
        self.de_res_info.setMaximumSize(QSize(260, 50))
        self.de_res_info.setFont(font)
        self.de_res_info.setObjectName("de_res_info")
        self.de_resolution_layout.addWidget(self.de_res_info)
        self.de_resolution_box = QDoubleSpinBox(self.main_layout)
        self.de_resolution_box.setMinimumSize(QSize(100, 40))
        self.de_resolution_box.setMaximumSize(QSize(200, 80))
        self.de_resolution_box.setFont(font)
        self.de_resolution_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.de_resolution_box.setAlignment(Qt.AlignCenter)
        self.de_resolution_box.setMaximum(999999999.99)
        self.de_resolution_box.setProperty("value", 1.0)
        self.de_resolution_box.setPalette(palette)
        self.de_resolution_box.setObjectName("de_resolution_box")
        self.de_resolution_layout.addWidget(self.de_resolution_box)
        self.de_layout.addLayout(self.de_resolution_layout)
        self.detector_layout.addLayout(self.de_layout)
        self.e_layout = QVBoxLayout()
        self.e_layout.setObjectName("e_layout")
        self.e_detector_info = QLabel(self.main_layout)
        self.e_detector_info.setMinimumSize(QSize(0, 30))
        self.e_detector_info.setMaximumSize(QSize(16777215, 60))
        self.e_detector_info.setFont(font)
        self.e_detector_info.setAlignment(Qt.AlignCenter)
        self.e_detector_info.setObjectName("e_detector_info")
        self.e_layout.addWidget(self.e_detector_info)
        self.e_element_box = QComboBox(self.main_layout)
        self.e_element_box.setMinimumSize(QSize(0, 40))
        self.e_element_box.setMaximumSize(QSize(16777215, 60))
        self.e_element_box.setPalette(palette)
        self.e_element_box.setFont(font)
        self.e_element_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.e_element_box.setObjectName("e_element_box")
        self.e_element_box.addItem("")
        self.e_element_box.addItem("")
        self.e_element_box.addItem("")
        self.e_layout.addWidget(self.e_element_box)
        self.e_thickness_layout = QHBoxLayout()
        self.e_thickness_layout.setObjectName("e_thickness_layout")
        self.e_thick_info = QLabel(self.main_layout)
        self.e_thick_info.setMinimumSize(QSize(130, 50))
        self.e_thick_info.setMaximumSize(QSize(260, 80))
        self.e_thick_info.setFont(font)
        self.e_thick_info.setObjectName("e_thick_info")
        self.e_thickness_layout.addWidget(self.e_thick_info)
        self.e_thickness_box = QDoubleSpinBox(self.main_layout)
        self.e_thickness_box.setMinimumSize(QSize(100, 40))
        self.e_thickness_box.setMaximumSize(QSize(200, 80))
        self.e_thickness_box.setFont(font)
        self.e_thickness_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.e_thickness_box.setAlignment(Qt.AlignCenter)
        self.e_thickness_box.setMaximum(999999999.99)
        self.e_thickness_box.setProperty("value", 2000.0)
        self.e_thickness_box.setPalette(palette)
        self.e_thickness_box.setObjectName("e_thickness_box")
        self.e_thickness_layout.addWidget(self.e_thickness_box)
        self.e_layout.addLayout(self.e_thickness_layout)
        self.e_resolution_layout = QHBoxLayout()
        self.e_resolution_layout.setObjectName("e_resolution_layout")
        self.e_res_info = QLabel(self.main_layout)
        self.e_res_info.setMinimumSize(QSize(130, 50))
        self.e_res_info.setMaximumSize(QSize(260, 50))
        self.e_res_info.setFont(font)
        self.e_res_info.setObjectName("e_res_info")
        self.e_resolution_layout.addWidget(self.e_res_info)
        self.e_resolution_box = QDoubleSpinBox(self.main_layout)
        self.e_resolution_box.setMinimumSize(QSize(100, 40))
        self.e_resolution_box.setMaximumSize(QSize(200, 80))
        self.e_resolution_box.setFont(font)
        self.e_resolution_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.e_resolution_box.setAlignment(Qt.AlignCenter)
        self.e_resolution_box.setMaximum(999999999.99)
        self.e_resolution_box.setProperty("value", 1.0)
        self.e_resolution_box.setPalette(palette)
        self.e_resolution_box.setObjectName("e_resolution_box")
        self.e_resolution_layout.addWidget(self.e_resolution_box)
        self.e_layout.addLayout(self.e_resolution_layout)
        self.detector_layout.addLayout(self.e_layout)
        self.telescope_layout.addLayout(self.detector_layout)
        self.verticalLayout.addLayout(self.telescope_layout)
        self.distance_layout = QHBoxLayout()
        self.distance_layout.setObjectName("distance_layout")
        self.distance_label = QLabel(self.main_layout)
        self.distance_label.setMinimumSize(QSize(370, 40))
        self.distance_label.setMaximumSize(QSize(370, 80))
        self.distance_label.setObjectName("beam_span_label")
        self.distance_layout.addWidget(self.distance_label)
        self.distance_box = QDoubleSpinBox(self.main_layout)
        self.distance_box.setMinimumSize(QSize(150, 40))
        self.distance_box.setMaximumSize(QSize(16777215, 80))
        self.distance_box.setPalette(palette)
        self.distance_box.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.distance_box.setAlignment(Qt.AlignCenter)
        self.distance_box.setMaximum(999999.0)
        self.distance_box.setSingleStep(0.1)
        self.distance_box.setObjectName("distance_box")
        self.distance_layout.addWidget(self.distance_box)
        self.verticalLayout.addLayout(self.distance_layout)
        self.radius_layout = QHBoxLayout()
        self.radius_layout.setObjectName("radius_layout")
        self.radius_label = QLabel(self.main_layout)
        self.radius_label.setMinimumSize(QSize(370, 40))
        self.radius_label.setMaximumSize(QSize(370, 80))
        self.radius_label.setObjectName("radius_label")
        self.radius_layout.addWidget(self.radius_label)
        self.radius_box = QDoubleSpinBox(self.main_layout)
        self.radius_box.setMinimumSize(QSize(150, 40))
        self.radius_box.setMaximumSize(QSize(16777215, 80))
        self.radius_box.setPalette(palette)
        self.radius_box.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.radius_box.setAlignment(Qt.AlignCenter)
        self.radius_box.setMaximum(999999.0)
        self.radius_box.setSingleStep(0.1)
        self.radius_box.setObjectName("collimator_box")
        self.radius_layout.addWidget(self.radius_box)
        self.verticalLayout.addLayout(self.radius_layout)
        self.integrator_layout = QHBoxLayout()
        self.integrator_layout.setObjectName("integrator_layout")
        self.integrator_label = QLabel(self.main_layout)
        self.integrator_label.setMinimumSize(QSize(370, 40))
        self.integrator_label.setMaximumSize(QSize(355, 80))
        self.integrator_label.setObjectName("integrator_label")
        self.integrator_layout.addWidget(self.integrator_label)
        self.integrator_line = QLineEdit(self.main_layout)
        self.integrator_line.setMinimumSize(QSize(150, 40))
        self.integrator_line.setMaximumSize(QSize(16777215, 80))
        self.integrator_line.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.integrator_line.setAlignment(Qt.AlignCenter)
        self.integrator_line.setObjectName("integrator_line")
        self.integrator_layout.addWidget(self.integrator_line)
        self.integrator_correct_label = QLabel(self.main_layout)
        self.integrator_correct_label.setMinimumSize(QSize(0, 40))
        self.integrator_correct_label.setMaximumSize(QSize(120, 80))
        self.integrator_correct_label.setObjectName("integrator_correct_label")
        self.integrator_layout.addWidget(self.integrator_correct_label)
        self.verticalLayout.addLayout(self.integrator_layout)
        self.misscalc_layout = QHBoxLayout()
        self.misscalc_layout.setObjectName("misscalc_layout")
        self.misscalc_label = QLabel(self.main_layout)
        self.misscalc_label.setMinimumSize(QSize(370, 40))
        self.misscalc_label.setMaximumSize(QSize(370, 80))
        self.misscalc_label.setObjectName("misscalc_label")
        self.misscalc_layout.addWidget(self.misscalc_label)
        self.misscalc_line = QLineEdit(self.main_layout)
        self.misscalc_line.setMinimumSize(QSize(150, 40))
        self.misscalc_line.setMaximumSize(QSize(16777215, 80))
        self.misscalc_line.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.misscalc_line.setAlignment(Qt.AlignCenter)
        self.misscalc_line.setObjectName("misscalc_line")
        self.misscalc_layout.addWidget(self.misscalc_line)
        self.misscalc_correct_label = QLabel(self.main_layout)
        self.misscalc_correct_label.setMinimumSize(QSize(0, 40))
        self.misscalc_correct_label.setMaximumSize(QSize(120, 80))
        self.misscalc_correct_label.setObjectName("misscalc_correct_label")
        self.misscalc_layout.addWidget(self.misscalc_correct_label)
        self.verticalLayout.addLayout(self.misscalc_layout)
        self.intconst_layout = QHBoxLayout()
        self.intconst_layout.setObjectName("intconst_layout")
        self.intconst_label = QLabel(self.main_layout)
        self.intconst_label.setMinimumSize(QSize(370, 40))
        self.intconst_label.setMaximumSize(QSize(370, 80))
        self.intconst_label.setObjectName("intconst_label")
        self.intconst_layout.addWidget(self.intconst_label)
        self.intconst_line = QLineEdit(self.main_layout)
        self.intconst_line.setMinimumSize(QSize(150, 40))
        self.intconst_line.setMaximumSize(QSize(16777215, 80))
        self.intconst_line.setStyleSheet("background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);")
        self.intconst_line.setAlignment(Qt.AlignCenter)
        self.intconst_line.setObjectName("intconst_line")
        self.intconst_layout.addWidget(self.intconst_line)
        self.intconst_correct_label = QLabel(self.main_layout)
        self.intconst_correct_label.setMinimumSize(QSize(0, 40))
        self.intconst_correct_label.setMaximumSize(QSize(120, 80))
        self.intconst_correct_label.setObjectName("intconst_correct_label")
        self.intconst_layout.addWidget(self.intconst_correct_label)
        self.verticalLayout.addLayout(self.intconst_layout)
        self.apply_button = QPushButton(self.main_layout)
        self.apply_button.setMinimumSize(QSize(0, 70))
        self.apply_button.setMaximumSize(QSize(16777215, 120))
        self.apply_button.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.apply_button)
        self.horizontalLayout.addWidget(self.main_layout)
        spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        FileConfigWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(FileConfigWindow)
        QMetaObject.connectSlotsByName(FileConfigWindow)

    def retranslateUi(self, FileConfigWindow):
        _translate = QCoreApplication.translate
        FileConfigWindow.setWindowTitle(_translate("FileConfigWindow", "dSigma — Experiment file config editor"))
        self.beam_label.setText(_translate("FileConfigWindow", BEAM_INFO))
        self.beam_line.setPlaceholderText(_translate("FileConfigWindow", "Examples: d, alpha, 16O"))
        self.beam_correct_label.setText(_translate("FileConfigWindow", OKAY_INFO))
        self.target_label.setText(_translate("FileConfigWindow", TARGET_INFO))
        self.target_line.setPlaceholderText(_translate("FileConfigWindow", "Examples: Pb208, Li-7, proton"))
        self.target_correct_label.setText(_translate("FileConfigWindow", OKAY_INFO))
        self.energy_label.setText(_translate("FileConfigWindow", ENERGY_INFO))
        self.energy_box.setSuffix(_translate("FileConfigWindow", " MeV"))
        self.angle_label.setText(_translate("FileConfigWindow", ANGLE_INFO))
        self.angle_box.setSuffix(_translate("FileConfigWindow", " deg."))
        self.angle_correct_label.setText(_translate("FileConfigWindow", OKAY_INFO))
        self.telescope_info.setText(_translate("FileConfigWindow", "Telescope"))
        self.de_detector_info.setText(_translate("FileConfigWindow", "dE Detector"))
        self.de_element_box.setItemText(0, _translate("FileConfigWindow", "Si"))
        self.de_element_box.setItemText(1, _translate("FileConfigWindow", "HpGe"))
        self.de_element_box.setItemText(2, _translate("FileConfigWindow", "C3H6"))
        self.de_thick_info.setText(_translate("FileConfigWindow", THICKNESS_INFO))
        self.de_thickness_box.setSuffix(_translate("FileConfigWindow", " mkm"))
        self.de_res_info.setText(_translate("FileConfigWindow", RESOLUTION_INFO))
        self.de_resolution_box.setSuffix(_translate("FileConfigWindow", " keV"))
        self.e_detector_info.setText(_translate("FileConfigWindow", "E Detector"))
        self.e_element_box.setItemText(0, _translate("FileConfigWindow", "Si"))
        self.e_element_box.setItemText(1, _translate("FileConfigWindow", "HpGe"))
        self.e_element_box.setItemText(2, _translate("FileConfigWindow", "C3H6"))
        self.e_thick_info.setText(_translate("FileConfigWindow", THICKNESS_INFO))
        self.e_thickness_box.setSuffix(_translate("FileConfigWindow", " mkm"))
        self.e_res_info.setText(_translate("FileConfigWindow", RESOLUTION_INFO))
        self.e_resolution_box.setSuffix(_translate("FileConfigWindow", " keV"))
        self.distance_label.setText(_translate("FileConfigWindow", DISTANCE_INFO))
        self.distance_box.setSuffix(_translate("FileConfigWindow", " mm"))
        self.radius_label.setText(_translate("FileConfigWindow", RADIUS_INFO))
        self.radius_box.setSuffix(_translate("FileConfigWindow", " mm"))
        self.integrator_label.setText(_translate("FileConfigWindow", INTEGRATOR_INFO))
        self.integrator_line.setPlaceholderText(_translate("FileConfigWindow", "Examples: 1.23e+10, 1345678"))
        self.integrator_correct_label.setText(_translate("FileConfigWindow", OKAY_INFO))
        self.misscalc_label.setText(_translate("FileConfigWindow", MISSCALC_INFO))
        self.misscalc_line.setPlaceholderText(_translate("FileConfigWindow", "Examples: 1.23e+10, 1345678"))
        self.misscalc_correct_label.setText(_translate("FileConfigWindow", OKAY_INFO))
        self.intconst_label.setText(_translate("FileConfigWindow", INTCONST_INFO))
        self.intconst_line.setPlaceholderText(_translate("FileConfigWindow", "Examples: 1.23e-10, 0.000012"))
        self.intconst_correct_label.setText(_translate("FileConfigWindow", OKAY_INFO))
        self.apply_button.setText(_translate("FileConfigWindow", "Apply Changes"))


class FileEditor(QMainWindow, Ui_FileConfigWindow):
    def __init__(self, file: Matrix) -> None:
        # WINDOW SETUP
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        # DATA
        self.matrix = file

        self.beam = file.experiment.beam
        self.target = file.experiment.target
        self.energy = file.experiment.beam_energy
        self.angle = file.angle

        self.de_elm = file.electronics.de_detector.madeof
        self.de_thick = file.electronics.de_detector.thickness
        self.de_res = file.electronics.de_detector.resolution
        self.e_elm = file.electronics.e_detector.madeof
        self.e_thick = file.electronics.e_detector.thickness
        self.e_res = file.electronics.e_detector.resolution

        self.distance = file.electronics.distance
        self.radius = file.electronics.collimator_radius

        self.integrator = file.integrator_counts
        self.misscalc = file.misscalculation
        self.intconst = file.integrator_constant

        self.set_all()

        # EVENT HANDLING
        self.beam_line.textChanged.connect(self.nuclei_check)
        self.target_line.textChanged.connect(self.nuclei_check)

        self.energy_box.valueChanged.connect(self.energy_check)
        self.angle_box.valueChanged.connect(self.angle_check)

        self.de_thickness_box.valueChanged.connect(self.electronics_check)
        self.de_resolution_box.valueChanged.connect(self.electronics_check)
        self.e_thickness_box.valueChanged.connect(self.electronics_check)
        self.e_resolution_box.valueChanged.connect(self.electronics_check)
        self.distance_box.valueChanged.connect(self.electronics_check)
        self.radius_box.valueChanged.connect(self.electronics_check)

        self.integrator_line.textChanged.connect(self.float_check)
        self.misscalc_line.textChanged.connect(self.float_check)
        self.intconst_line.textChanged.connect(self.float_check)

        self.apply_button.clicked.connect(self.apply)

    def set_all(self) -> None:
        self.beam_line.setText(str(self.beam))
        self.target_line.setText(str(self.target))
        self.energy_box.setProperty("value", self.energy)
        self.angle_box.setProperty("value", self.angle)

        self.de_thickness_box.setProperty("value", self.de_thick)
        self.de_resolution_box.setProperty("value", self.de_res * 1e3)
        self.e_thickness_box.setProperty("value", self.e_thick)
        self.e_resolution_box.setProperty("value", self.e_res * 1e3)

        self.distance_box.setProperty("value", self.distance)
        self.radius_box.setProperty("value", self.radius)

        self.integrator_line.setText(str(self.integrator))
        self.misscalc_line.setText(str(self.misscalc))
        self.intconst_line.setText(str(self.intconst))

    def nuclei_check(self) -> None:
        try:
            pretend = Nuclei.from_string(self.beam_line.text())
            self.beam_correct_label.setText(OKAY_INFO)

            self.handle_changes(
                self.beam, pretend, self.beam_label, BEAM_INFO
            )
        except:
            self.beam_correct_label.setText(NOT_OKAY_INFO)

        try:
            pretend = Nuclei.from_string(self.target_line.text())
            self.target_correct_label.setText(OKAY_INFO)

            self.handle_changes(
                self.target, pretend, self.target_label, TARGET_INFO
            )
        except:
            self.target_correct_label.setText(NOT_OKAY_INFO)

    def energy_check(self) -> None:
        self.handle_changes(
            self.energy, self.energy_box.value(),
            self.energy_label, ENERGY_INFO
        )

    def angle_check(self) -> None:
        self.handle_changes(
            self.angle, self.angle_box.value(),
            self.angle_label, ANGLE_INFO
        )

        if self.angle_box.value() > 0 and self.angle_box.value() < 180:
            self.angle_correct_label.setText(OKAY_INFO)
        else:
            self.angle_correct_label.setText(NOT_OKAY_INFO)

    def electronics_check(self) -> None:
        self.handle_changes(
            self.de_thick, self.de_thickness_box.value(),
            self.de_thick_info, THICKNESS_INFO
        )

        self.handle_changes(
            self.de_res * 1e3, self.de_resolution_box.value(),
            self.de_res_info, RESOLUTION_INFO
        )

        self.handle_changes(
            self.e_thick, self.e_thickness_box.value(),
            self.e_thick_info, THICKNESS_INFO
        )

        self.handle_changes(
            self.e_res * 1e3, self.e_resolution_box.value(),
            self.e_res_info, RESOLUTION_INFO
        )

        self.handle_changes(
            self.distance, self.distance_box.value(),
            self.distance_label, DISTANCE_INFO
        )

        self.handle_changes(
            self.radius, self.radius_box.value(),
            self.radius_label, RADIUS_INFO
        )

    def float_check(self) -> None:
        self.handle_changes(
            str(self.integrator), self.integrator_line.text(),
            self.integrator_label, INTEGRATOR_INFO
        )
        try:
            pretend = float(self.integrator_line.text())
            self.integrator_correct_label.setText(OKAY_INFO)
        except:
            self.integrator_correct_label.setText(NOT_OKAY_INFO)

        self.handle_changes(
            str(self.misscalc), self.misscalc_line.text(),
            self.misscalc_label, MISSCALC_INFO
        )
        try:
            pretend = float(self.misscalc_line.text())
            self.misscalc_correct_label.setText(OKAY_INFO)
        except:
            self.misscalc_correct_label.setText(NOT_OKAY_INFO)

        self.handle_changes(
            str(self.intconst), self.intconst_line.text(),
            self.intconst_label, INTCONST_INFO
        )
        try:
            pretend = float(self.intconst_line.text())
            self.intconst_correct_label.setText(OKAY_INFO)
        except:
            self.intconst_correct_label.setText(NOT_OKAY_INFO)

    def handle_changes(self, ethalon, value, label, info) -> None:
        if ethalon != value:
            label.setText('*' + info)
        else:
            label.setText(info)

    def apply(self) -> None:
        self.save_physics()
        self.save_electronics()
        self.save_details()

        self.close()

    def save_physics(self) -> None:
        if '*' in self.beam_label.text() and OKAY_INFO in self.beam_correct_label.text():
            self.matrix.experiment.beam = Nuclei.from_string(self.beam_line.text())

        if '*' in self.target_label.text() and OKAY_INFO in self.target_correct_label.text():
            self.matrix.experiment.target = Nuclei.from_string(self.target_line.text())

        if '*' in self.energy_label.text():
            self.matrix.experiment.beam_energy = self.energy_box.value()

        if '*' in self.angle_label.text() and OKAY_INFO in self.angle_correct_label.text():
            self.matrix.angle = self.angle_box.value()

    def save_electronics(self) -> None:
        if '*' in self.de_thick_info.text():
            self.matrix.electronics.de_detector.thickness = self.de_thickness_box.value()

        if '*' in self.de_res_info.text():
            self.matrix.electronics.de_detector.resolution = self.de_resolution_box.value() * 1e-3

        if '*' in self.e_thick_info.text():
            self.matrix.electronics.e_detector.thickness = self.e_thickness_box.value()

        if '*' in self.e_res_info.text():
            self.matrix.electronics.e_detector.resolution = self.e_resolution_box.value() * 1e-3

        if '*' in self.distance_label.text():
            self.matrix.electronics.distance = self.distance_box.value()

        if '*' in self.radius_label.text():
            self.matrix.electronics.collimator_radius = self.radius_box.value()

    def save_details(self) -> None:
        if '*' in self.integrator_label.text() and OKAY_INFO in self.integrator_correct_label.text():
            self.matrix.integrator_counts = float(self.integrator_line.text())

        if '*' in self.misscalc_label.text() and OKAY_INFO in self.misscalc_correct_label.text():
            self.matrix.misscalculation = float(self.congruence_line.text())

        if '*' in self.intconst_label.text() and OKAY_INFO in self.intconst_correct_label.text():
            self.matrix.integrator_constant = float(self.intconst_line.text())


if __name__ == "__main__":
    pass
