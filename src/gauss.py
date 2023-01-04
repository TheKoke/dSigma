import math
import numpy as np
from src.spectr import Spectr

class Gaussograph:
    '''
    Takes the info, and tries to
    draw gaussian distrubution around.
    '''

    def __init__(self, spectr: Spectr) -> None:
        pass

    def get_all_peaks(self) -> list[int]:
        pass

    def calc_fwhm(self) -> np.float128:
        pass

    def calc_areas(self) -> list[np.float128]:
        pass

class GaussDistrubution:
    '''
    W(x) = 1/(sqrt(2pi * sigma^2) * exp{-(x - <x>)^2 / 2sigma^2)}
    sigma = sqrt(1/(N - 1) * Sum(i, N, (x(i) - <x>)^2)
    sigma -> dispersion
    '''
    def __init__(self, data: np.ndarray) -> None:
        self.data = data

    def arithmetic_mean(self) -> np.float128:
        return self.data.mean(dtype=np.float128)

    def dispersion(self) -> np.float128:
        mean = self.arithmetic_mean()

        return np.sqrt(((self.data - mean) ** 2).sum() / (len(self.data) - 1), dtype=np.float128)

    def w(self) -> np.float128:
        constpart = 1 / np.sqrt(2 * math.pi * self.dispersion() ** 2, dtype=np.float128)
        exppart = np.exp(-1 * (self.data - self.arithmetic_mean() ** 2) / 2 * self.dispersion(), dtype=np.float128)

        return constpart * exppart