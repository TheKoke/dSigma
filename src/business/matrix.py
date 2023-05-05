import numpy as np
from parsing import USBParser
from spectrums import Spectrum


def rescale(numbers: np.ndarray) -> np.ndarray:
    transform_const = 255 / (numbers.max() - numbers.min())
    result = numbers - numbers.min()

    return result * transform_const


class Locus:
    def __init__(self, name: str, matrix: np.ndarray, dots: list[tuple[int, int]]) -> None:
        self.name = name
        self.matrix = matrix
        self.dots = dots

        self.boundaries = self.define_boundaries() # [dE(min), dE(max), E(min), E(max)]

    def define_boundaries(self) -> list[int]:
        pass

    def to_spectrum(self) -> Spectrum:
        pass


class Matrix:
    def __init__(self, parser: USBParser) -> None:
        self.angle = parser.get_angle()
        self.integrator_count = parser.get_integrator_counts()
        self.misscalculation = parser.get_misscalculation()

        self.locuses = parser.take_locuses()
        self.reactions = parser.reactor.all_reactions()

        self.numbers = parser.get_matrix()

    def bright_up(self, amount: int) -> np.ndarray:
        return rescale(self.numbers + amount)

    def bright_down(self, amount: int) -> np.ndarray:
        return rescale(self.numbers - amount)

    def cut(self) -> np.ndarray:
        pass

    def generate_locus_spectrum(self, locus: Locus) -> Spectrum:
        pass


if __name__ == '__main__':
    pass