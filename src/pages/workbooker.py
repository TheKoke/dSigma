from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WorkbookRevWindow(QMainWindow):
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


if __name__ == '__main__':
    app = QApplication()
    wind = WorkbookRevWindow()
    wind.show()
    app.exec()