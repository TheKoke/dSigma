import os
from business.matrix import USBParser


class Sleuth:
    def __init__(self, main_directory: str) -> None:
        self.main = main_directory

    def all_parsers(self) -> list[USBParser]:
        files = self.sort()
        return [USBParser(file) for file in files]

    def usb_names(self) -> list[str]:
        directories = os.listdir(self.main)
        sifted = self.only_files(directories)
        return [file for file in sifted if '.usb' in file]

    def sort(self) -> list[str]:
        directories = os.listdir(self.main)
        return sorted(self.only_usb(directories))
    
    def only_usb(self, dirs: list[str]) -> list[str]:
        sifted = self.only_files(dirs)
        return [self.main + '/' + file for file in sifted if '.usb' in file]
    
    def only_files(self, dirs: list[str]) -> list[str]:
        return [direc for direc in dirs if '.' if direc]
    

if __name__ == '__main__':
    pass
