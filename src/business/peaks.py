from __future__ import annotations

import numpy
from abc import ABC, abstractmethod
from business.smoothing import QH353


class PeakFunction(ABC):
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        self._mu = mu
        self._fwhm = fwhm
        self._area = area

    @property
    def mu(self) -> float:
        '''
        Center of peak.
        '''
        return self._mu
    
    @property
    def fwhm(self) -> float:
        '''
        Full-width on half maximum of peak.
        '''
        return self._fwhm
    
    @property
    def dispersion(self) -> float:
        '''
        Dispersion of peak.
        '''
        return self._fwhm / (2 * numpy.sqrt(2 * numpy.log(2)))
    
    @property
    def area(self) -> float:
        '''
        Area under peak.
        '''
        return self._area
    
    def to_workbook(self) -> str:
        return f'Peak on mu=({round(self.mu, 3)}) with fwhm=({round(self.fwhm, 3)}) and area under peak=({round(self.area, 3)})'
    
    def three_sigma(self) -> numpy.ndarray:
        return numpy.linspace(-3 * self.dispersion + self._mu, 3 * self.dispersion + self._mu, 100)

    @abstractmethod
    def func(self, x: numpy.ndarray = None) -> numpy.ndarray:
        pass


class Gaussian(PeakFunction):
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        super().__init__(mu, fwhm, area)

    def __str__(self) -> str:
        func = 'G(x) = '
        func += f'{numpy.round(self.area, 3)} / (sqrt(2pi * {numpy.round(self.dispersion, 3)}) * '
        func += f'exp(-(x - {numpy.round(self.mu, 3)})^2 / 2{numpy.round(self.dispersion, 3)})'

        return func
    
    def func(self, x: numpy.ndarray = None) -> numpy.ndarray:
        if x is None:
            x = self.three_sigma()

        constant = 2 * self._area * numpy.sqrt(numpy.log(2) / (numpy.pi * numpy.power(self._fwhm, 2)))
        array = numpy.exp(-4 * numpy.log(2) * numpy.power(x - self._mu, 2) / numpy.power(self._fwhm, 2))
        return constant * array
    

class Lorentzian(PeakFunction):
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        super().__init__(mu, fwhm, area)

    def __str__(self) -> str:
        func = 'L(x) = '
        func += f'2 * {round(self._area, 3)} / pi'
        func += f'* [{numpy.round(self._fwhm, 3)} / ((x - {round(self._mu)})^2 + {round(self._fwhm, 3)}^2)]'

        return func
    
    def func(self, x: numpy.ndarray = None) -> numpy.ndarray:
        if x is None:
            x = self.three_sigma()

        constant = 2 * self._area / numpy.pi
        brackets = self._fwhm / (4 * (x - self._mu) ** 2 + self._fwhm ** 2)
        return constant * brackets


class Trapezoid:
    def __init__(self, base1: float, base2: float, height: float) -> None:
        self.__b1 = base1
        self.__b2 = base2
        self.__h = height

    @property
    def small_base(self) -> float:
        return min(self.__b1, self.__b2)
    
    @property
    def big_base(self) -> float:
        return max(self.__b1, self.__b2)
    
    @property
    def height(self) -> float:
        return self.__h
    
    def area(self) -> float:
        return self.__h * (self.__b1 + self.__b2) / 2


class PeakAnalyzer:
    def __init__(self, spectrum: numpy.ndarray, mu_index: int) -> None:
        self.mu_index = mu_index
        self.spectrum = spectrum
        self.smoothed = QH353().smooth(self.spectrum)

    def approximate(self) -> PeakFunction:
        minimum_width = 3

        start, stop = self.mu_index - minimum_width // 2 + 1, self.mu_index + minimum_width // 2 + 2
        is_over_border = start < 0 or stop > len(self.spectrum)

        chi_squares = []

        while not self.is_increasing(chi_squares, minimum_width) and not is_over_border:
            chi2 = self.fit_gauss(start, stop)

            if not numpy.isnan(chi2) and not numpy.isinf(chi2):
                chi_squares.append(chi2)

            start -= 1
            stop += 1
            is_over_border = start < 0 or stop > len(self.spectrum)

        if len(chi_squares) < minimum_width:
            return PeakFunction(self.mu_index, numpy.nan, numpy.nan)

        start = start + minimum_width - 1
        stop = stop - minimum_width

        xdata = numpy.arange(start + 1, stop + 1)
        ydata = self.spectrum[start: stop]

        area, dispersion, center = self.describe_gauss(xdata, ydata, self.mu_index)
        return PeakFunction(center, dispersion, area)
    
    def fit_gauss(self, start: int, stop: int) -> float:
        xdata = numpy.arange(start + 1, stop + 1)
        ydata = self.smoothed[start: stop]

        area, dispersion, center = PeakAnalyzer.describe_gauss(xdata, ydata, self.mu_index)
        return PeakAnalyzer.chi_square(area, ydata.sum())
    
    def is_increasing(self, chi: list[float], minimum_width: int) -> bool:
        if len(chi) <= minimum_width:
            return False
        
        lasts = chi[-minimum_width:]
        for i in range(len(lasts) - 1):
            if lasts[i] > lasts[i + 1]:
                return False

        return True
    
    @staticmethod
    def describe_gauss(xdata: numpy.ndarray, ydata: numpy.ndarray, center: int) -> tuple[float, float, float]:
        xdata = numpy.power(xdata - center, 2)
        ydata[ydata == 0] = 1
        ydata = numpy.log(ydata)
        weights = ydata / ydata.sum()

        a_hat, b_hat = PeakAnalyzer.least_squares(xdata, ydata, weights)

        fsquare = -4 * numpy.log(2) / a_hat
        if fsquare < 0:
            return (numpy.nan, numpy.nan, numpy.nan)
        
        fwhm = numpy.sqrt(fsquare)
        area = numpy.exp(b_hat) / 2 * numpy.sqrt(numpy.pi * fsquare / numpy.log(2))

        return area, fwhm, center
    
    @staticmethod
    def describe_lorentz(xdata: numpy.ndarray, ydata: numpy.ndarray, center: int) -> tuple[float, float, float]:
        xdata = numpy.power(xdata - center, 2)
        ydata[ydata == 0] = 0.001
        ydata = 1 / ydata

        a_hat, b_hat = PeakAnalyzer.least_squares(xdata, ydata)
        if (a_hat <= 0 and b_hat >= 0) or (a_hat >= 0 and b_hat <= 0):
            return (numpy.nan, numpy.nan, numpy.nan)
        
        fwhm = numpy.sqrt(4 * b_hat / a_hat)
        area = numpy.pi * fwhm / (2 * b_hat)

        return area, fwhm, center
    
    @staticmethod
    def least_squares(x: numpy.ndarray, y: numpy.ndarray, w: numpy.ndarray = None) -> tuple[float, float]:
        if w is None:
            w = numpy.ones_like(x)

        system = numpy.array([[1, (w * x).sum()], [(w * x).sum(), (w * numpy.power(x, 2)).sum()]])
        righthand = numpy.array([(w * y).sum(), (w * x * y).sum()])

        solutions = numpy.linalg.solve(system, righthand)
        return (solutions[1], solutions[0])

    @staticmethod
    def chi_square(theory: numpy.ndarray, experimenthal: numpy.ndarray) -> float:
        return (experimenthal - theory) ** 2 / theory


if __name__ == '__main__':
    pass
