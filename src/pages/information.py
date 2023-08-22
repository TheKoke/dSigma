from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel


class InformWindow(QDialog):
    def __init__(self, message: str) -> None:
        super().__init__()

        self.setWindowTitle("Info About.")
        self.setWindowIcon(QIcon('./icon.ico'))
        self.setFixedSize(300, 100)

        label = QLabel(text=message)
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout(self)
        layout.addWidget(label)


if __name__ == '__main__':
    pass
