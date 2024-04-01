import numpy as np


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
        if len(self.points) == 0:
            return np.zeros(256).tolist()

        taken = self.select()
        result = []

        for i in range(0, len(taken), 2):
            e_position = taken[i].e_position

            de_start = min(taken[i].de_position, taken[i + 1].de_position)
            de_stop = max(taken[i].de_position, taken[i + 1].de_position)

            result.append(self.matrix[de_start:de_stop + 1, e_position].sum())

        left_bound = taken[0].e_position
        right_bound = taken[-1].e_position

        return np.zeros(left_bound).tolist() + result + np.zeros(len(self.matrix) - right_bound - 1).tolist()

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
    def __init__(self, matrix: np.ndarray, points: list[tuple[int, int]]) -> None:
        self.__points = points
        self.__projector = Extrapolation(matrix, points)
        
    @property
    def points(self) -> list[tuple[int, int]]:
        return self.__points
    
    def to_workbook(self) -> str:
        report = ''
        for i in self.__points:
            report += f'\t(E: {i[0]}; dE: {i[1]})\n'

        return report

    def to_spectrum(self) -> list[int]:
        return self.__projector.to_spectrum()
    

if __name__ == '__main__':
    pass
