import numpy as np
from parsing import USBParser
from spectrums import Spectrum

class Matrix:
    def __init__(self, parser: USBParser) -> None:
        self.angle = parser.get_angle()
        self.integrator_count = parser.get_integrator_counts()
        self.misscalculation = parser.get_misscalculation()

        self.locuses = parser.take_locuses()
        self.reactions = parser.take_all_reactions()

        self.numbers = parser.get_matrix()

    def rescale(self) -> np.ndarray:
        transform_const = 255 / (self.numbers.max() - self.numbers.min())
        result = self.numbers - self.numbers.min()

        return result * transform_const

    def bright_up(self, amount: int) -> np.ndarray:
        pass

    def bright_down(self, amount: int) -> np.ndarray:
        pass

    def cut(self) -> np.ndarray:
        pass

    def generate_locus_spectrum(self, locus: str) -> Spectrum:
        pass


if __name__ == '__main__':
    pass