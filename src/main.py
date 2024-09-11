import sys
import pyuac

from PyQt5.QtWidgets import QApplication

from pages.welcomer import WelcomeWindow


if __name__ == '__main__':
    # if not pyuac.isUserAdmin():
    #     pyuac.runAsAdmin()
    # else:
    #     app = QApplication(sys.argv)
    #     wind = WelcomeWindow()

    #     wind.show()
    #     app.exec()
    app = QApplication(sys.argv)
    wind = WelcomeWindow()

    wind.show()
    app.exec()
