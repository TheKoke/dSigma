import numpy as np
from parsing import *
from spectrums import Spectrum


def rescale(numbers: np.ndarray) -> np.ndarray:
    transform_const = 255 / (numbers.max() - numbers.min())
    result = numbers - numbers.min()

    return result * transform_const


class Locus:
    def __init__(self, name: str, matrix: np.ndarray, points: list[tuple[int, int]]) -> None:
        self.name = name
        self.matrix = matrix
        self.points = points

        self.boundaries = self.define_boundaries() # [dE(min), dE(max), E(min), E(max)]

    def define_boundaries(self) -> list[int]:
        Emax = 0; Emin = len(self.matrix)
        dEmax = 0; dEmin = len(self.matrix)

        for point in self.points:
            Emax = max(Emax, point[0])
            Emin = min(Emin, point[0])

            dEmax = max(dEmax, point[1])
            dEmin = min(dEmin, point[1])

        return [dEmin, dEmax, Emin, Emax]

    def to_spectrum(self) -> list[int]:
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
    
    def generate_all_locuses(self) -> list[Locus]:
        return [Locus(particle, self.numbers, self.locuses[particle]) for particle in self.locuses]

    def generate_locus_spectrum(self, particle: str) -> Spectrum:
        if particle not in self.locuses:
            return None
        
        locus = next(item for item in self.generate_all_locuses() if item.name == particle)
        return Spectrum(locus.to_spectrum())


if __name__ == '__main__':
    pass