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
        From locus gives an spectrum of projection to E-axis.
        Returns spectrum as list.
        '''
        if len(self.points) == 0:
            return []
        
        upper, lower = self.break_up()

        ceiling = self.select(upper)
        floor = self.select(lower)

        left_border = sorted(self.step(upper[0], lower[0]), key=lambda x: x.e_position)
        right_border = sorted(self.step(upper[-1], lower[-1]), key=lambda x: x.e_position)

        ceiling, floor = self.handle_borders(ceiling, floor, left_border, right_border)

        return self.project(ceiling, floor)

    def handle_borders(self, ceiling: list[Cell], floor: list[Cell], left: list[Cell], right: list[Cell]) -> tuple[list[Cell], list[Cell]]:
        '''
        Method that handles border of locus and glue upper and lower borders.
        '''
        up_start, up_stop, low_start, low_stop = self.find_body(ceiling, floor)

        if up_start < low_start:
            mask = left[:low_start]
            mask.extend(ceiling)

            ceiling = mask

        if up_start > low_start:
            mask = left[:up_start]
            mask.extend(floor)

            floor = mask

        if up_stop - len(ceiling) < low_stop - len(floor):
            floor.extend(right[up_stop - len(ceiling):])

        if up_stop - len(ceiling) > low_stop - len(floor):
            ceiling.extend(right[low_stop - len(floor):])

        return (ceiling[:len(floor)], floor[:len(ceiling)])
    
    def find_body(self, ceiling: list[Cell], floor: list[Cell]) -> tuple[int, int, int, int]:
        '''
        Method for finding covered area between ceiling and floor of locus.\n
        Returns tuple of:\n
        (ceiling start index, ceiling stop index, floor start index, floor stop index).
        '''
        up_start, up_stop = 0, len(ceiling) - 1
        low_start, low_stop = 0, len(floor) - 1

        if ceiling[0].e_position > floor[0].e_position:
            low_start = ceiling[0].e_position - floor[0].e_position
        
        if ceiling[0].e_position < floor[0].e_position:
            up_start = floor[0].e_position - ceiling[0].e_position

        if ceiling[-1].e_position > floor[-1].e_position:
            up_stop = len(ceiling) - (ceiling[-1].e_position - floor[-1].e_position) - 1

        if ceiling[-1].e_position < floor[-1].e_position:
            low_stop = len(floor) - (floor[-1].e_position - ceiling[-1].e_position) - 1

        return (up_start, up_stop, low_start, low_stop)

    def project(self, ceiling: list[Cell], floor: list[Cell]) -> list[int]:
        '''
        Method for projecting locus to E-axis.
        '''
        spectrum = list()
        for i in range(len(ceiling)):
            e_index = ceiling[i].e_position
            de_start = min(ceiling[i].de_position, floor[i].de_position)
            de_stop = max(ceiling[i].de_position, floor[i].de_position) + 1

            spectrum.append(self.matrix[de_start:de_stop, e_index].sum())

        return spectrum

    def select(self, queue: list[Cell]) -> list[Cell]:
        '''
        Taking points for each column of matrix through all locus.\n
        Returns the result as list of Cells.
        '''
        collected = []
        for i in range(len(queue) - 1):
            collected.extend(self.step(queue[i], queue[i + 1])[:-1])

        return collected

    def step(self, start: Cell, stop: Cell) -> list[Cell]:
        '''
        Method, that extrapolates dots between 2 points.\n
        Returns list of covered cells.
        '''
        if start.e_position == stop.e_position:
            return [start if start.de_position < stop.de_position else stop]

        system = np.array([[start.e_position, 1], [stop.e_position, 1]])
        righthand = np.array([start.de_position, stop.de_position])
        line = np.linalg.solve(system, righthand)

        covered = []
        for x in range(start.e_position, stop.e_position):
            covered.append(Cell(x, round(line[0] * x + line[1])))

        return covered
    
    def break_up(self) -> tuple[list[Cell], list[Cell]]:
        '''
        Function to get upper- and lower-bounds of locus.
        '''
        for i in range(1, len(self.points)):
            if self.points[i - 1].e_position > self.points[i].e_position:
                break
        
        upper = sorted(self.points[i:], key=lambda x: x.e_position)
        lower = sorted(self.points[:i], key=lambda x: x.e_position)
        return (upper, lower)


class Locus:
    def __init__(self, particle: Nuclei, matrix: np.ndarray, points: list[tuple[int, int]]) -> None:
        self.__particle = particle
        self.__rpf = Extrapolation(matrix, points)

    @property
    def particle(self) -> Nuclei:
        return self.__particle

    def to_spectrum(self) -> list[int]:
        return self.__rpf.to_spectrum()


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