import math
import numpy
from matrix import Matrix

class Gaussograph:
    '''
    Takes the info from locus, and tries to
    draw gaussian distrubution around.
    '''

    def __init__(self, matrix: Matrix, ranges: tuple[float, float]) -> None:
        pass

    def check_to_peaks(self) -> int:
        pass

class GaussDistrubution:
    '''
    W(x) = 1/(sqrt(2pi * sigma^2) * exp{-(x - <x>)^2/2sigma^2)}
    sigma -> dispersion
    sigma = sqrt(1/(N - 1) * Sum(i, N, (x(i) - <x>)^2)
    '''
    def __init__(self, data: list[float]) -> None:
        self.data = data

    def arithmetic_mean(self) -> float:
        return sum(self.data) / len(self.data)

    def dispersion(self) -> float:
        mean = self.arithmetic_mean()
        return math.sqrt(sum(map(lambda x: (x - mean) ** 2, self.data)) / (len(self.data) - 1))

    def w(self, x: float) -> float:
        constpart = 1 / math.sqrt(2 * math.pi * self.dispersion() ** 2)
        exppart = math.exp(-1 * (x - self.arithmetic_mean() ** 2) / (2 * self.dispersion()))

        return constpart * exppart

    def probability_density(self) -> list[float]:
        return [self.w(self.data[i]) for i in range(len(self.data))]