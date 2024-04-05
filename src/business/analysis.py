import numpy
from scipy.optimize import curve_fit

from business.smoothing import QH353
from business.electronics import Telescope
from business.physics import Reaction, Struggling, CrossSection



class Gaussian:
    def __init__(self, mu: float, sigma: float, area: float) -> None:
        self.__mu = mu
        self.__dispersion = sigma
        self.__area = area

    @property
    def mu(self) -> float:
        return self.__mu
    
    @property
    def dispersion(self) -> float:
        return self.__dispersion
    
    @property
    def area(self) -> float:
        return self.__area
    
    @property
    def fwhm(self) -> float:
        return self.__dispersion * (2 * numpy.sqrt(2 * numpy.log(2)))
    
    def to_workbook(self) -> str:
        return f'Peak on mu=({round(self.mu, 3)}) with fwhm=({round(self.fwhm, 3)}) and area under peak=({round(self.area, 3)})'

    def __str__(self) -> str:
        func = 'G(x) = '
        func += f'{numpy.round(self.area, 3)} / (sqrt(2pi * {numpy.round(self.dispersion, 3)}) * '
        func += f'exp(-(x - {numpy.round(self.mu, 3)})^2 / 2{numpy.round(self.dispersion, 3)})'

        return func

    def three_sigma(self) -> numpy.ndarray:
        return numpy.linspace(-3 * self.__dispersion + self.__mu, 3 * self.__dispersion + self.__mu, 100)
    
    def function(self) -> numpy.ndarray:
        constant = self.__area / numpy.sqrt(2 * numpy.pi * numpy.power(self.__dispersion, 2))
        array = numpy.exp(-numpy.power(self.three_sigma() - self.__mu, 2) / (2 * numpy.power(self.__dispersion, 2)))
        return constant * array
    

class Lorentzian:
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        self.mu = mu
        self.fwhm = fwhm
        self.area = area

    def to_workbook(self) -> str:
        return f'Peak on mu=({round(self.mu, 3)}) with fwhm=({round(self.fwhm, 3)}) and area under peak=({round(self.area, 3)})'

    def __str__(self) -> str:
        func = 'L(x) = '
        func += f'2 * {round(self.area, 3)} / pi'
        func += f'* [{numpy.round(self.fwhm, 3)} / ((x - {round(self.mu)})^2 + {round(self.fwhm, 3)}^2)]'

        return func
    
    def dispersion(self) -> float:
        return self.fwhm / (2 * numpy.sqrt(2 * numpy.log(2)))
    
    def three_sigma(self) -> numpy.ndarray:
        sigma = self.dispersion()
        return numpy.linspace(-5 * sigma + self.mu, 5 * sigma + self.mu, 50)
    
    def function(self) -> numpy.ndarray:
        constant = 2 * self.area / numpy.pi
        brackets = self.fwhm / (4 * (self.three_sigma() - self.mu) ** 2 + self.fwhm ** 2)

        return constant * brackets


class PeakAnalyzer:
    def __init__(self, spectrum: numpy.ndarray, mu_index: int) -> None:
        self.spectrum = spectrum
        self.smoothed = QH353().smooth(self.spectrum)
        self.mu_index = mu_index

    def approximate(self) -> Gaussian:
        minimum_width = 5

        start, stop = self.mu_index - minimum_width // 2 + 1, self.mu_index + minimum_width // 2 + 2
        is_over_border = start < 0 or stop > len(self.spectrum)

        chi_squares = []

        while not self.is_increasing(chi_squares, minimum_width) and not is_over_border:
            chi2 = self.fit_gauss(self.mu_index, start, stop)
            chi_squares.append(chi2)

            start -= 1
            stop += 1
            is_over_border = start < 0 or stop > len(self.spectrum)

        start = self.mu_index - minimum_width + 1
        stop = self.mu_index + minimum_width - 1

        xdata = numpy.arange(start + 1, stop + 1)
        ydata = self.spectrum[start: stop]

        area, dispersion, center = self.describe_gauss(xdata, ydata)
        center += self.mu_index
        return Gaussian(center, dispersion, area)
    
    def fit_gauss(self, peak: int, start: int, stop: int) -> float:
        xdata = numpy.arange(start + 1, stop + 1)
        ydata = self.smoothed[start: stop]

        area, dispersion, center = self.describe_gauss(xdata, ydata)
        center += peak

        y_hat = PeakAnalyzer.gauss(area, dispersion, center, xdata)
        return PeakAnalyzer.collective_chi_square(y_hat, ydata)
    
    def describe_gauss(self, xdata: numpy.ndarray, ydata: numpy.ndarray) -> tuple[float, float, float]:
        weights = ydata / ydata.sum()
        xdata = numpy.power(xdata - xdata[len(xdata) // 2], 2)
        ydata[ydata == 0] = 1
        ydata = numpy.log(ydata)

        d_hat, a_hat = PeakAnalyzer.least_squares(xdata, ydata, weights)
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
    
    @staticmethod
    def least_squares(x: numpy.ndarray, y: numpy.ndarray, w: numpy.ndarray) -> tuple[float, float]:
        system = numpy.array([[1, (w * x).sum()], [(w * x).sum(), (w * numpy.power(x, 2)).sum()]])
        righthand = numpy.array([(w * y).sum(), (w * x * y).sum()])

        solutions = numpy.linalg.solve(system, righthand)
        return (solutions[1], solutions[0])
    
    @staticmethod
    def gauss(a: float, d: float, c: float, x: float) -> float:
        return a / numpy.sqrt(2 * numpy.pi * (d ** 2)) * numpy.exp(- (x - c) ** 2 / (2 * (d ** 2)))

    @staticmethod
    def collective_chi_square(theory: numpy.ndarray, experimenthal: numpy.ndarray) -> float:
        return ((experimenthal - theory) ** 2).sum() / len(theory)


class Spectrum:
    def __init__(self, reaction: Reaction, angle: float, electronics: Telescope, data: list[int]) -> None:
        self.__angle = angle
        self.__reaction = reaction
        self.__electronics = electronics

        self.__data = numpy.array(data)

        self.__scale_shift = 0
        self.__scale_value = 0

        self.__peaks: dict[float, Gaussian] = dict()

    @property
    def is_calibrated(self) -> bool:
        return len(self.energy_view) != 0
    
    @property
    def gamma_widths(self) -> list[float]:
        self_widths = numpy.array(self.__reaction.residual.wigner_widths[:len(self.__reaction.residual_states)])
        detector_resolution = self.__electronics.e_detector.resolution
        return numpy.sqrt(self_widths ** 2 + detector_resolution ** 2).tolist()
    
    @property
    def angle(self) -> float:
        return self.__angle
    
    @property
    def reaction(self) -> Reaction:
        return self.__reaction
    
    @property
    def electronics(self) -> Telescope:
        return self.__electronics
    
    @property
    def data(self) -> numpy.ndarray:
        return self.__data
    
    @property
    def energy_view(self) -> numpy.ndarray:
        if self.__scale_shift == 0 and self.__scale_value == 0:
            return numpy.array([])
        
        return self.__scale_value * numpy.arange(1, len(self.__data) + 1) + self.__scale_shift
    
    @property
    def scale_shift(self) -> float:
        return self.__scale_shift
    
    @scale_shift.setter
    def scale_shift(self, val: float) -> None:
        self.__scale_shift = val
        self.__peaks.clear()

    @property
    def scale_value(self) -> float:
        return self.__scale_value
    
    @scale_value.setter
    def scale_value(self, val: float) -> None:
        if val < 0:
            raise ValueError('Scale value of channel can not be negative or equal to 0.')
        
        self.__scale_value = val
        self.__peaks.clear()

    @property
    def peaks(self) -> dict[float, Gaussian]:
        return self.__peaks.copy()
    
    def to_workbook(self) -> str:
        report = "Spectrum of -> \n"
        report += f"{self.__reaction} reaction,\n"
        report += f"With {self.__reaction.beam} energy = {round(self.__reaction.beam_energy, 3)} MeV.\n"
        report += f"At laboratory angle = {round(self.__angle, 3)} degrees.\n\n"
        report += f"Calibrated by: E(ch) = {round(self.__scale_value, 3)}*ch + {round(self.__scale_shift, 3)}.\n\n"
        report += f"Peaks of spectrum:\n"

        for state in self.peaks:
            report += self.peaks[state].to_workbook() + '\n'

        return report
    
    def add_peak(self, state: float, peak: Gaussian) -> None:
        if not self.is_calibrated:
            raise ValueError('Spectrum must be calibrated before approximating peaks.')
        
        if state not in self.reaction.residual_states:
            raise ValueError(f'There is no state of residual nuclei of reaction same as {state}')
        
        self.__peaks[state] = peak


class SpectrumAnalyzer:
    def __init__(self, spectrums: list[Spectrum]) -> None:
        self.spectrums = sorted(spectrums, key=lambda x: x.angle)
        self.dsigma = self.__create_cross_section()

    def __create_cross_section(self) -> CrossSection:
        angles = numpy.array(self.angles())
        return CrossSection(self.spectrums[0].reaction, angles)
    
    def angles(self) -> list[float]:
        return [sp.angle for sp in self.spectrums]

    def approximate(self, index: int) -> None:
        spectrum = self.spectrums[index]
        if not spectrum.is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')

        states = spectrum.reaction.residual_states

        found = self.find_peaks(index)
        for i in range(len(found)):
            gauss = found[i].approximate()
            if numpy.isnan(gauss.area) or numpy.isnan(gauss.fwhm):
                continue

            if numpy.isinf(gauss.area) or numpy.isinf(gauss.fwhm):
                continue

            spectrum.add_peak(states[i], gauss)
            
    def find_peaks(self, index: int) -> list[PeakAnalyzer]:
        spectrum = self.spectrums[index]
        if not spectrum.is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')
        
        theories = self.theory_peaks(index)
        
        collected = []
        for i in range(len(theories)):
            k, e0 = spectrum.scale_value, spectrum.scale_shift

            pretend_channel = int((theories[i] - e0) / k)
            if pretend_channel <= len(self.spectrums[index].data) * 0.02:
                continue

            collected.append(PeakAnalyzer(spectrum.data, pretend_channel))

        return collected
    
    def theory_peaks(self, index: int) -> list[float]:
        current = self.spectrums[index]

        piercing = current.electronics.de_detector
        stopping = current.electronics.e_detector

        de_bete_bloch = Struggling(current.reaction.fragment, piercing.madeof_nuclei)
        e_bete_bloch = Struggling(current.reaction.fragment, stopping.madeof_nuclei)

        likely_peaks = []
        for state in current.reaction.residual_states:
            initial = current.reaction.fragment_energy(state, current.angle)

            de_loss = de_bete_bloch.energy_loss(initial, piercing.thickness * 1e-4, piercing.density)
            if initial < de_loss:
                break

            e_loss = e_bete_bloch.energy_loss(initial - de_loss, stopping.thickness * 1e-4, stopping.density)
            if initial - de_loss < e_loss:
                likely_peaks.append(initial - de_loss)
            else:
                likely_peaks.append(e_loss)

        return likely_peaks
    
    def calibrate(self, index: int, anchors_indexes: tuple[int], states: tuple[float]) -> None:
        current = self.spectrums[index]

        anchors_indexes = sorted(anchors_indexes, reverse=True)
        theories = self.theory_peaks(index)

        first_state_index = current.reaction.residual.states.index(states[0])
        second_state_index = current.reaction.residual.states.index(states[1])

        matrix = numpy.array([[anchors_indexes[0], 1], [anchors_indexes[1], 1]])
        right_side = numpy.array([theories[first_state_index], theories[second_state_index]])

        solution = numpy.linalg.solve(matrix, right_side)
        current.scale_value, current.scale_shift = solution[0], solution[1]


if __name__ == '__main__':
    pass
