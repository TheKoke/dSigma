from business.matrix import Matrix
from business.parsing import USBParser


class CSCollection:
    def __init__(self) -> None:
        pass


class SpectrumCollection:
    def __init__(self) -> None:
        pass


class MatrixCollection:
    def __init__(self, parsers: list[USBParser]) -> None:
        self.parsers = parsers

    def collect_matrixes(self) -> list[Matrix]:
        pass


if __name__ == '__main__':
    pass
