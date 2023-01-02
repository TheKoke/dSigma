import numpy

class USBParser:
    def __init__(self, path: str) -> None:
        self.path = path
        self.binary_sizes = (0, 256 ** 2)

    def set_binary(self) -> None:
        pass

    def parse_to_txt(self) -> str:
        pass

    def parse_to_csv(self) -> str:
        pass

    def __generate_path(self) -> str:
        pass