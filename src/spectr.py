import numpy as np
from scipy.signal import find_peaks
from src.matrix import Matrix

class Gaussian:
    '''
    W(x) = 1/(sqrt(2pi * sigma) * exp{-(x - <x>)^2 / 2sigma})
    sigma = sqrt(1/(N - 1) * Sum(i, N, (x(i) - <x>)^2)
    sigma -> dispersion
    '''
    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        pass

    def peak_center(self) -> np.float64:
        return self.x[self.y.argmax()]

    def area(self) -> np.float64:
        return self.full_width_half_might() / np.sqrt(2 * np.log(2)) \
            * self.max_height() * np.sqrt(np.pi / 2)

    def full_width_half_might(self) -> np.float64:
        return self.dispersion() / (2 * np.sqrt(2 * np.log(2)))

    def up_shift(self) -> np.float64:
        return self.y.min()

    def max_height(self) -> np.float64:
        return self.y.max()

    def probability(self) -> np.ndarray:
        constant = self.area() / (self.full_width_half_might() * np.sqrt(np.pi / (4 * np.log(2))))

        exp_constant = -1 * (4 * np.log(2)) / (self.full_width_half_might() ** 2)
        array_part = (self.x - self.peak_center()) ** 2

        return self.up_shift() + constant * np.exp(exp_constant * array_part)
    
    def arithmetic_mean(self) -> np.float64:
        return self.x.mean()

    def dispersion(self) -> np.float64:
        mean = self.arithmetic_mean()
        return np.sum((self.x - mean) ** 2, dtype=np.float64) / (len(self.x) - 1)

class Parabola:
    pass

class Spectr:
    def __init__(self, source: Matrix) -> None:
        self.source = source
        self.is_channelview = True

        self.data = self.__calc()
        self.clean_up()

        self.peaks = self.__all_peaks()
        self.gausses = self.__gaussians()
    
    def to_energy_view(self) -> None:
        pass

    def to_channelview(self) -> None:
        pass

    def clean_up(self, collapse: np.float64) -> str:
        # 1.164 = collapse threshold for Li7(d,d)Li7 reaction
        pass

    def calc_fwhm(self) -> np.ndarray:
        pass

    def calc_areas(self) -> np.ndarray:
        pass

    def to_workbook(self) -> str:
        pass

    def __gaussians(self) -> np.ndarray:
        return np.array(
            [Gaussian(self.data[0, i - 5: i + 5], self.data[1, i - 5 : i + 5]) for i in self.peaks]
        )

    def __all_peaks(self) -> np.ndarray:
        return np.array(find_peaks(self.data, height=100, distance=10)[0])

    def __calc(self) -> np.ndarray:
        result = np.array([np.arange(0, 256, 1, dtype=np.uint32), np.zeros(self.source.dim, dtype=np.uint32)])

        for i in range(result.shape[0]):
            result[1, i] = self.source.components[i, :].sum()

        return result