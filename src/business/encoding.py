import struct
import numpy as np

from business.matrix import Matrix, Spectrum, Locus


class Encoder:
    def __init__(self, matrix: Matrix, directory: str) -> None:
        self.matrix = matrix
        self.directory = directory

    def write_down(self) -> None:
        path = self.generate_file_name()
        buffer = open(path, 'wb')

    def generate_file_name(self) -> str:
        pass


class Decoder:
    def __init__(self, path: str) -> None:
        self.buffer = open(path, 'rb')


if __name__ == '__main__':
    pass
