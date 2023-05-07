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
    
    def cut_rectangle(self) -> np.ndarray:
        return self.matrix[self.boundaries[0]: self.boundaries[1], self.boundaries[2]: self.boundaries[3]]
    
    def cut_locus_shape(self) -> list[list[int]]:
        pass

    def to_spectrum(self) -> list[int]:
        pass


class Matrix:
    def __init__(self, parser: USBParser) -> None:
        self.parser = parser
        self.numbers = self.parser.get_matrix()

    def bright_up(self, amount: int) -> np.ndarray:
        return rescale(self.numbers + amount)

    def bright_down(self, amount: int) -> np.ndarray:
        return rescale(self.numbers - amount)
    
    def generate_all_locuses(self) -> list[Locus]:
        locuses = self.parser.take_locuses()
        return [Locus(particle, self.numbers, locuses[particle]) for particle in locuses]

    def generate_locus_spectrum(self, particle: str) -> Spectrum:
        if particle not in self.parser.take_locuses():
            return None
        
        locus = next(item for item in self.generate_all_locuses() if item.name == particle)
        return Spectrum(
            self.parser.reactor.take_reaction(particle), 
            self.parser.get_integrator_counts(), 
            self.parser.get_misscalculation(),
            locus.to_spectrum()
        )


if __name__ == '__main__':
    pass