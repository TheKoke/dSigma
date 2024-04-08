from pages.matrixograph import Matrixograph

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QLineEdit, QFileDialog


class Ui_Welcome(object):
    def setupUi(self, dSigma):
        dSigma.setObjectName("dSigma")
        dSigma.resize(400, 300)
        dSigma.setMinimumSize(QSize(400, 300))
        dSigma.setMaximumSize(QSize(400, 300))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        dSigma.setFont(font)
        dSigma.setAutoFillBackground(False)
        dSigma.setStyleSheet("background-color: rgb(0, 0, 127);\ncolor: rgb(255, 255, 255);")
        self.verticalLayout = QVBoxLayout(dSigma)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QFrame(dSigma)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.type_label = QLabel(self.frame)
        self.type_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(11)
        self.type_label.setFont(font)
        self.type_label.setAlignment(Qt.AlignCenter)
        self.type_label.setObjectName("type_label")
        self.verticalLayout_2.addWidget(self.type_label)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input = QLineEdit(self.frame)
        self.input.setMinimumSize(QSize(200, 20))
        self.input.setMaximumSize(QSize(16777215, 30))
        self.input.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.input.setObjectName("input")
        self.horizontalLayout.addWidget(self.input)
        self.file_button = QPushButton(self.frame)
        self.file_button.setMinimumSize(QSize(20, 20))
        self.file_button.setMaximumSize(QSize(40, 30))
        self.file_button.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.file_button.setObjectName("file_button")
        self.horizontalLayout.addWidget(self.file_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.enter_button = QPushButton(self.frame)
        self.enter_button.setMinimumSize(QSize(0, 60))
        font = QFont()
        font.setPointSize(12)
        self.enter_button.setFont(font)
        self.enter_button.setStyleSheet("background-color: rgb(85, 85, 127);")
        self.enter_button.setObjectName("enter_button")
        self.verticalLayout_2.addWidget(self.enter_button)
        self.verticalLayout.addWidget(self.frame)
        self.frame_2 = QFrame(dSigma)
        self.frame_2.setMaximumSize(QSize(16777215, 60))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.version_label = QLabel(self.frame_2)
        self.version_label.setMaximumSize(QSize(16777215, 20))
        self.version_label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.version_label.setObjectName("version_label")
        self.verticalLayout_3.addWidget(self.version_label)
        self.info_label = QLabel(self.frame_2)
        self.info_label.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setPointSize(11)
        self.info_label.setFont(font)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setObjectName("info_label")
        self.verticalLayout_3.addWidget(self.info_label)
        self.verticalLayout.addWidget(self.frame_2)

        self.retranslateUi(dSigma)
        QMetaObject.connectSlotsByName(dSigma)

    def retranslateUi(self, dSigma):
        _translate = QCoreApplication.translate
        dSigma.setWindowTitle(_translate("dSigma", "dSigma — Welcome Page"))
        self.type_label.setText(_translate("dSigma", "Please, type the path to directory of E-dE matrices"))
        self.input.setPlaceholderText(_translate("dSigma", "Example: C:\\Users\\User\\Directory\\"))
        self.file_button.setText(_translate("dSigma", "..."))
        self.enter_button.setText(_translate("dSigma", "Enter"))
        self.version_label.setText(_translate("dSigma", "dSigma v0.3.0"))
        self.info_label.setText(_translate("dSigma", "LLENR application for analyzing spectres"))


class WelcomeWindow(QDialog, Ui_Welcome):
    def __init__(self) -> None:
        # SETUP OF WINDOW
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("./icon.ico"))

        self.path = ''

        # EVENT HANDLING
        self.file_button.clicked.connect(self.take_directory)
        self.enter_button.clicked.connect(self.start)

    def take_directory(self) -> None:
        paths = QFileDialog.getExistingDirectory(self)
        self.input.setText(paths)
        self.path = paths

    def start(self) -> None:
        if self.path == '':
            return

        self.window = Matrixograph(self.path)
        self.window.show()
        self.hide()


if __name__ == "__main__":
    pass
