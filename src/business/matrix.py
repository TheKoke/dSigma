import numpy as np

from business.parsing import USBParser
from business.physics import Nuclei, Reaction
from business.analysis import Analyzer, Spectrum
from business.electronics import Telescope


class Cell:
    '''
    This class is just little structure to save point in matrix.
    '''
    def __init__(self, e_position: int, de_position: int) -> None:
        self.__e_position = e_position
        self.__de_position = de_position

    def __repr__(self) -> str:
        return f'[E: {self.e_position}, dE: {self.de_position}]'

    @property
    def e_position(self) -> int:
        return self.__e_position
    
    @property
    def de_position(self) -> int:
        return self.__de_position


class Extrapolation:
    '''
    Class for implementing Locus cutting in matrix.\n
    Uses Extrapolation algortihm. 
    '''
    def __init__(self, matrix: np.ndarray, points: list[tuple[int, int]]) -> None:
        self.matrix = matrix
        self.points = [Cell(*point) for point in points]

    def to_spectrum(self) -> list[int]:
        '''
        Method for projecting cutted locus to E-axis and get the spectrum.
        '''
        taken = self.select()
        result = []

        for i in range(0, len(taken), 2):
            e_position = taken[i].e_position

            de_start = min(taken[i].de_position, taken[i + 1].de_position)
            de_stop = max(taken[i].de_position, taken[i + 1].de_position)

            result.append(self.matrix[de_start:de_stop + 1, e_position].sum())

        return result

    def select(self) -> list[Cell]:
        '''
        Taking points for each column of matrix through all locus.\n
        Returns the result as list of Cells.
        '''
        collected = []
        for i in range(len(self.points) - 1):
            collected.extend(self.step(self.points[i], self.points[i + 1]))

        return sorted(collected, key=lambda x: x.e_position * len(self.matrix) + x.de_position)

    def step(self, first: Cell, second: Cell) -> list[Cell]:
        '''
        Method, that extrapolates dots between 2 points.\n
        Returns list of covered cells.
        '''
        if first.e_position == second.e_position:
            return [first, second]

        system = np.array([[first.e_position, 1], [second.e_position, 1]])
        righthand = np.array([first.de_position, second.de_position])
        line = np.linalg.solve(system, righthand)

        covered = []
        start = min(first.e_position, second.e_position)
        stop = max(first.e_position, second.e_position)

        for x in range(start, stop):
            covered.append(Cell(x, round(line[0] * x + line[1])))

        return covered


class Locus:
    def __init__(self, particle: Nuclei, matrix: np.ndarray, points: list[tuple[int, int]]) -> None:
        self.__particle = particle
        self.__algo = Extrapolation(matrix, points)

    @property
    def particle(self) -> Nuclei:
        return self.__particle

    def to_spectrum(self) -> list[int]:
        return self.__algo.to_spectrum()


class Demo:
    def __init__(self, parser: USBParser) -> None:
        self.parser = parser

    def spectrums(self) -> list[list[int]]:
        alls = self.locuses()
        return [self.locus_spectrum(each) for each in alls]

    def locus_spectrum(self, points: list[tuple[int, int]]) -> list[int]:
        matrix = self.matrix()
        return Extrapolation(matrix, points).to_spectrum()
    
    def locuses(self) -> list[list[tuple[int, int]]]:
        alls = self.parser.take_locuses()
        return [alls[each] for each in alls]
    
    def matrix(self) -> np.ndarray:
        return self.parser.get_matrix()


class Matrix:
    def __init__(self, parser: USBParser, electronics: Telescope) -> None:
        self.parser = parser
        self.electronics = electronics

        self.numbers = self.parser.get_matrix()

    @property
    def angle(self) -> float:
        return self.parser.get_angle()

    @property
    def integrator_counts(self) -> int:
        return self.parser.get_integrator_counts()
    
    @property
    def misscalculation(self) -> float:
        return self.parser.get_misscalculation()
    
    def all_spectres(self) -> dict[Nuclei, Spectrum]:
        locuses = self.generate_all_locuses()
        return {each.particle : each.to_spectrum() for each in locuses}

    def generate_locus_spectrum(self, locus: Locus) -> Spectrum:
        reaction = self.__build_reaction(locus.particle)
        data = locus.to_spectrum()
        return Spectrum(reaction, self.angle, self.electronics, data)
    
    def generate_all_locuses(self) -> list[Locus]:
        alls = self.parser.take_locuses()
        return [Locus(each, self.numbers, alls[each]) for each in alls]
    
    def __build_reaction(self, fragment: Nuclei) -> Reaction:
        beam = self.parser.parse_beam()
        target = self.parser.parse_target()
        energy = self.parser.get_beam_energy()

        return Reaction(beam, target, fragment, energy)


if __name__ == '__main__':
    pass