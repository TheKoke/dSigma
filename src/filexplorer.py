import os
from business.matrix import Decoder


class Sleuth:
    def __init__(self, main_directory: str) -> None:
        self.main = main_directory
    
    def all_decoders(self) -> list[Decoder]:
        directories = os.listdir(self.main)
        files = self.only_ds(directories)
        return [Decoder(file) for file in files]
    
    def ds_names(self) -> list[str]:
        directories = os.listdir(self.main)
        sifted = self.only_files(directories)
        return [file for file in sifted if '.ds' in file]

    def sort(self) -> list[str]:
        directories = os.listdir(self.main)
        return sorted(self.only_ds(directories))
    
    def only_ds(self, dirs: list[str]) -> list[str]:
        sifted = self.only_files(dirs)
        return [self.main + '/' + file for file in sifted if '.ds' in file]
    
    def only_files(self, dirs: list[str]) -> list[str]:
        return [direc for direc in dirs if '.' if direc]
    

if __name__ == '__main__':
    pass
