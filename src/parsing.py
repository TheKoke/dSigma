import numpy

class USBParser:
    def __init__(self, path: str) -> None:
        self.path = path
        self.binary_sizes = (0, 256 ** 2)

    def set_binary(self) -> None:
        pass

    def parse_to_txt(self) -> str:
        return self.__generate_path('txt')

    def parse_to_csv(self) -> str:
        return self.__generate_path('csv')

    def __generate_path(self, extension: str) -> str:
        folder = '\\'.join(self.path.split('\\')[:-1])
        name = ''.join(self.path.split('\\')[-1].split('.')[:-1])

        return folder + '\\' + name + '.' + extension