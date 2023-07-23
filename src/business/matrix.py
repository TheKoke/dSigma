import numpy as np

from business.parsing import USBParser
from business.analysis import Spectrum
from business.yard import NucleiConverter
from business.electronics import Telescope
from business.physics import Nuclei, Reaction, PhysicalExperiment, CrossSection


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
    '''
    Class that represents Locus in Matrix.
    '''
    def __init__(self, particle: Nuclei, matrix: np.ndarray, points: list[tuple[int, int]]) -> None:
        self.__particle = particle
        self.__points = points
        self.__projector = Extrapolation(matrix, points)

    @property
    def particle(self) -> Nuclei:
        return self.__particle
        
    @property
    def points(self) -> list[tuple[int, int]]:
        return self.__points

    def to_spectrum(self) -> list[int]:
        return self.__projector.to_spectrum()


class Demo:
    def __init__(self, parser: USBParser) -> None:
        self.parser = parser
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
    
    def to_workbook(self) -> str:
        beam = NucleiConverter.to_string(self.parser.parse_beam())
        target = NucleiConverter.to_string(self.parser.parse_target())

        report = f'Matrix {self.parser.matrix_sizes} of -> \n'
        report += f'{target} + {beam} reaction at {self.parser.parse_beam_energy()} MeV.\n'
        report += f"Telescope's angle in lab-system: {self.angle} degrees.\n"
        report += f"Integrator's count: {self.integrator_counts}\n"
        report += f"Telescope's efficiency: {self.misscalculation}.\n"

        locuses = self.parser.take_locuses()
        for nuclei in locuses:
            report += f'Locus of {NucleiConverter.to_string(nuclei)}:\n'
            for i in locuses[nuclei]:
                report += f'\t(E: {i[0]}; dE: {i[1]})\n'

        return report

    def spectrums(self) -> list[list[int]]:
        alls = self.locuses()
        return [self.locus_spectrum(each) for each in alls]

    def locus_spectrum(self, points: list[tuple[int, int]]) -> list[int]:
        return Extrapolation(self.numbers, points).to_spectrum()
    
    def locuses(self) -> list[list[tuple[int, int]]]:
        alls = self.parser.take_locuses()
        return [alls[each] for each in alls]
    

class Matrix:
    def __init__(self, matrix: np.ndarray, experiment: PhysicalExperiment, electronics: Telescope, 
                 lab_angle: float, integrator: int, misscalculation: float) -> None:
        self.numbers = matrix

        self.experiment = experiment

        self.electronics = electronics
        self.angle = lab_angle

        self.integrator = integrator
        self.misscalculation = misscalculation

        self.locuses: list[Locus] = []
        self.spectrums: list[Spectrum] = []

    def add_locus(self, particle: Nuclei, points: list[tuple[int, int]]) -> None:
        self.locuses.append(Locus(particle, self.numbers, points))

    def spectrum_of(self, particle: Nuclei) -> Spectrum:
        if particle not in [locus.particle for locus in self.locuses]:
            raise ValueError(f'There is no locus of {particle} in matrix.')
        
        locus = next(locus for locus in self.locuses if locus.particle == particle)
        reaction = self.__build_reaction(particle)
        spectrum_data = locus.to_spectrum()

        self.spectrums.append(Spectrum(reaction, self.angle, self.electronics, spectrum_data))
        return self.spectrums[-1]

    def __build_reaction(self, fragment: Nuclei) -> Reaction:
        return self.experiment.create_reaction(fragment)
    

class MatrixAnalyzer:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self.matrixes = matrixes

    def collect_spectres(self, particle: Nuclei) -> list[Spectrum]:
        pass

    def cross_section_of(self, particle: Nuclei) -> np.ndarray:
        pass


if __name__ == '__main__':
    pass
