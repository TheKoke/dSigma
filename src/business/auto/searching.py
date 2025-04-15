import numpy
from business.peaks import PeakAnalyzer, Gaussian
    

class Pinnacle:
    def __init__(self, center: int, left: int, right: int) -> None:
        self.__center = center
        self.__left = left
        self.__right = right

    @property
    def center(self) -> int:
        return self.__center
    
    @property
    def left(self) -> int:
        return self.__left
    
    @property
    def right(self) -> int:
        return self.__right
    
    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f'Pinnacle(center:{self.__center})'


class Beagle:
    def __init__(self, spectrum: numpy.ndarray) -> None:
        self.spectrum = spectrum

    def peaks(self) -> list[Pinnacle]:
        pinnacles = []
        self.clear_background()

        copy = self.spectrum.copy()

        iters = 0
        while len(copy[copy != 0]) != 0 and iters < 5:
            peak = copy.argmax()

            if copy[peak - 1] == 0 or copy[peak + 1] == 0:
                copy[peak] = 0
                continue

            current_pinnacle = self.handle_peak(peak)
            pinnacles.append(current_pinnacle)

            copy[current_pinnacle.left: current_pinnacle.right + 1] = 0
            iters += 1

        return pinnacles
    
    def clear_background(self) -> numpy.ndarray:
        self.spectrum[:5] = 0
        self.spectrum[-5:] = 0
        self.spectrum[self.spectrum <= 2] = 0

        return self.spectrum

    def handle_peak(self, peak: int) -> Pinnacle:
        minimum_width = 3

        start, stop = peak - minimum_width // 2, peak + minimum_width // 2 + 1
        is_over_border = start < 0 or stop > len(self.spectrum)

        chi_squares = []

        while not PeakAnalyzer.is_increasing(chi_squares, minimum_width) and not is_over_border:
            chi2 = self.fit_gauss(peak, start, stop)
            chi_squares.append(chi2)

            start -= 1
            stop += 1
            is_over_border = start < 0 or stop > len(self.spectrum)

        start = start + numpy.argmin(chi_squares) - 1
        stop = stop - numpy.argmin(chi_squares)

        start = start if start >= 0 else 0
        stop = stop if stop < len(self.spectrum) else len(self.spectrum) - 1

        return Pinnacle(peak, start, stop)
    
    def fit_gauss(self, peak: int, start: int, stop: int) -> float:
        xdata = numpy.arange(start + 1, stop + 1)
        ydata = self.spectrum[start: stop]
        center = xdata[len(xdata) // 2]

        area, fwhm, center = PeakAnalyzer.describe_gauss(xdata, ydata, center)
        center += peak

        y_hat = Gaussian(center, fwhm, area).func(xdata)
        return PeakAnalyzer.chi_square(y_hat, ydata)


if __name__ == '__main__':
    pass