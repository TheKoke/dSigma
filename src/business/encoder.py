import struct
import numpy as np

from business.matrix import Matrix, Spectrum, Locus


class Encoder:
    def __init__(self, path: str, matrix: Matrix) -> None:
        self.path = path
        self.matrix = matrix

    def write_down(self) -> None:
        buffer = open(self.path, 'r')


class Decoder:
    def __init__(self, path: str) -> None:
        self.buffer = open(path, 'rb')


if __name__ == '__main__':
    pass
