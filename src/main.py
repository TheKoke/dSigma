import os
import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget

from pages import *
from business.matrix import Matrix
from business.parsing import USBParser
from business.analysis import Analyzer, Spectrum
from business.electronics import Telescope, Detector


class ExperimentConfig:
    def __init__(self) -> None:
        pass

    def get_electronics(self) -> Telescope:
        pass

    def gather_detector(self) -> Detector:
        pass


class Sleuth:
    def __init__(self, main_directory: str) -> None:
        self.main = main_directory

    def create_matrixes(self, electronics: Telescope) -> list[Matrix]:
        parsers = self.all_parsers()
        return [Matrix(parser, electronics) for parser in parsers]

    def all_parsers(self) -> list[USBParser]:
        files = self.sort()
        return [USBParser(file) for file in files]

    def sort(self) -> list[str]:
        directories = os.listdir(self.main)
        return self.only_usb(directories)
    
    def only_usb(self, dirs: list[str]) -> list[str]:
        sifted = self.only_files(dirs)
        return [file for file in sifted if '.usb' in file]
    
    def only_files(self, dirs: list[str]) -> list[str]:
        return [direc for direc in dirs if '.' if direc]


class WelcomeWindow(QDialog):
    def __init__(self) -> None:
        super().__init__()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = MainWindow()

    wind.show()
    app.exec()
