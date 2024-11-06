from business.physics import Nuclei

from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QColor
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QDialog,
    QVBoxLayout, QHBoxLayout, QComboBox, 
    QPushButton, QFrame, QLabel,
    QSpinBox, QLineEdit, QFileDialog
)


class Ui_NucleiWindow(object):
    def setupUi(self, ConfirmWindow):
        ConfirmWindow.setObjectName("ConfirmWindow")
        ConfirmWindow.resize(400, 300)
        ConfirmWindow.setMaximumSize(QSize(400, 300))
        ConfirmWindow.setStyleSheet("QPushButton{\nbackground-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);\n}\nQPushButton:pressed{\nbackground-color: rgb(55, 55, 97);\n}")
        self.verticalLayout = QVBoxLayout(ConfirmWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.info = QLabel(ConfirmWindow)
        self.info.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.info.setFont(font)
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setObjectName("info")
        self.verticalLayout.addWidget(self.info)
        self.boxes_layout = QHBoxLayout()
        self.boxes_layout.setObjectName("boxes_layout")
        self.nuclon_layout = QHBoxLayout()
        self.nuclon_layout.setObjectName("nuclon_layout")
        self.nuclon_info = QLabel(ConfirmWindow)
        self.nuclon_info.setMaximumSize(QSize(20, 40))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.nuclon_info.setFont(font)
        self.nuclon_info.setObjectName("nuclon_info")
        self.nuclon_layout.addWidget(self.nuclon_info)
        self.nuclon_box = QSpinBox(ConfirmWindow)
        self.nuclon_box.setMinimumSize(QSize(50, 60))
        font = QFont()
        font.setPointSize(20)
        self.nuclon_box.setFont(font)
        self.nuclon_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.nuclon_box.setMinimum(1)
        self.nuclon_box.setMaximum(300)
        self.nuclon_box.setProperty("value", 1)
        self.nuclon_box.setObjectName("nuclon_box")
        self.nuclon_layout.addWidget(self.nuclon_box)
        self.boxes_layout.addLayout(self.nuclon_layout)
        self.charge_layout = QHBoxLayout()
        self.charge_layout.setObjectName("charge_layout")
        self.charge_info = QLabel(ConfirmWindow)
        self.charge_info.setMaximumSize(QSize(20, 40))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.charge_info.setFont(font)
        self.charge_info.setObjectName("charge_info")
        self.charge_layout.addWidget(self.charge_info)
        self.charge_box = QSpinBox(ConfirmWindow)
        self.charge_box.setMinimumSize(QSize(50, 60))
        font = QFont()
        font.setPointSize(20)
        self.charge_box.setFont(font)
        self.charge_box.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);")
        self.charge_box.setMaximum(300)
        self.charge_box.setObjectName("charge_box")
        self.charge_layout.addWidget(self.charge_box)
        self.boxes_layout.addLayout(self.charge_layout)
        self.verticalLayout.addLayout(self.boxes_layout)
        self.nuclei_name = QLineEdit(ConfirmWindow)
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.nuclei_name.setFont(font)
        self.nuclei_name.setAlignment(Qt.AlignCenter)
        self.nuclei_name.setReadOnly(True)
        self.nuclei_name.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.nuclei_name)
        self.apply_button =  QPushButton(ConfirmWindow)
        self.apply_button.setMinimumSize(QSize(0, 60))
        self.apply_button.setFont(font)
        self.apply_button.setObjectName("apply_button")
        self.verticalLayout.addWidget(self.apply_button)
        self.cancel_button =  QPushButton(ConfirmWindow)
        self.cancel_button.setMinimumSize(QSize(0, 60))
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.verticalLayout.addWidget(self.cancel_button)

        self.retranslateUi(ConfirmWindow)
        QMetaObject.connectSlotsByName(ConfirmWindow)

    def retranslateUi(self, ConfirmWindow):
        _translate =  QCoreApplication.translate
        self.nuclon_info.setText(_translate("ConfirmWindow", "A:"))
        self.charge_info.setText(_translate("ConfirmWindow", "Z:"))
        self.apply_button.setText(_translate("ConfirmWindow", "Apply"))
        self.cancel_button.setText(_translate("ConfirmWindow", "Cancel"))


class ConfirmWindow(QDialog, Ui_NucleiWindow):
    def __init__(self) -> None:
        # SETUP WINDOW
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))
        self.setWindowTitle('Confirming Locus')
        self.info.setText('This is a locus of')

        # EVENT HADNLING
        self.charge_box.valueChanged.connect(self.show_nuclei)
        self.nuclon_box.valueChanged.connect(self.show_nuclei)
        self.apply_button.clicked.connect(self.close)
        self.cancel_button.clicked.connect(self.close)

    def show_nuclei(self) -> None:
        charge = self.charge_box.value()
        nuclon = self.nuclon_box.value()

        try:
            nuclei = Nuclei(charge, nuclon)
            self.nuclei_name.setText(nuclei.name)
        except:
            self.nuclei_name.setText("Doesn't exist!")


class DeleteWindow(QDialog, Ui_NucleiWindow):
    def __init__(self) -> None:
        # SETUP WINDOW
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))
        self.setWindowTitle('Deleting Locus')
        self.info.setText('Existing locus of')

        # EVENT HADNLING
        self.charge_box.valueChanged.connect(self.show_nuclei)
        self.nuclon_box.valueChanged.connect(self.show_nuclei)
        self.apply_button.clicked.connect(self.close)
        self.cancel_button.clicked.connect(self.close)

    def show_nuclei(self) -> None:
        charge = self.charge_box.value()
        nuclon = self.nuclon_box.value()

        try:
            nuclei = Nuclei(charge, nuclon)
            self.nuclei_name.setText(nuclei.name)
        except:
            self.nuclei_name.setText("Doesn't exist!")


if __name__ == '__main__':
    pass
