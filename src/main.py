import sys
from PyQt5.QtWidgets import QApplication
from pages.welcomer import WelcomeWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = WelcomeWindow()

    wind.show()
    app.exec()
