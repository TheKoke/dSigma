import numpy


def gauss(x: float, a: float, d: float, m: float) -> float:
    return a / numpy.sqrt(2 * numpy.pi * d ** 2) * numpy.exp(-(x - m) ** 2 / (2 * d ** 2))


def least_squares(x: numpy.ndarray, y: numpy.ndarray, w: numpy.ndarray) -> tuple[float, float]:
    system = numpy.array([[1, (w * x).sum()], [(w * x).sum(), (w * numpy.power(x, 2)).sum()]])
    righthand = numpy.array([(w * y).sum(), (w * x * y).sum()])

    solutions = numpy.linalg.solve(system, righthand)
    return (solutions[1], solutions[0])


def collective_chi_square(theory: numpy.ndarray, experimenthal: numpy.ndarray) -> float:
    return ((experimenthal - theory) ** 2).sum()
    

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

        while not self.is_increasing(chi_squares, minimum_width) and not is_over_border:
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

        area, dispersion, center = self.describe_gauss(xdata, ydata)
        center += peak

        y_hat = gauss(area, dispersion, center, xdata)
        return collective_chi_square(y_hat, ydata)
    
    def describe_gauss(self, xdata: numpy.ndarray, ydata: numpy.ndarray) -> tuple[float, float, float]:
        weights = ydata / ydata.sum()
        x_hat = numpy.power(xdata - xdata[len(xdata) // 2], 2)
        y_hat = ydata.copy()
        y_hat[y_hat == 0] = 1
        y_hat = numpy.log(y_hat)

        d_hat, a_hat = least_squares(x_hat, y_hat, weights)
        dispersion = numpy.sqrt(-1 / (2 * d_hat))
        area = numpy.exp(a_hat) * numpy.sqrt(2 * numpy.pi * dispersion ** 2)
        center = xdata[len(xdata) // 2]

        return area, dispersion, center
    
    def is_increasing(self, chi: list[float], minimum_width: int) -> bool:
        if len(chi) <= minimum_width:
            return False
        
        lasts = chi[-minimum_width:]
        for i in range(len(lasts) - 1):
            if lasts[i] > lasts[i + 1]:
                return False

        return True


if __name__ == '__main__':
    pass