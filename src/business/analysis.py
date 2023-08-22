import numpy as np

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
        return self.__dispersion / (2 * np.sqrt(2 * np.log(2)))
    
    def to_workbook(self) -> str:
        return f'Peak on mu=({self.mu}) with fwhm=({self.fwhm}) and area under peak=({self.area})'

    def __str__(self) -> str:
        func = 'G(x) = '
        func += f'{np.round(self.area, 3)} / (sqrt(2pi * {np.round(self.dispersion, 3)}) * '
        func += f'exp(-(x - {np.round(self.mu, 3)})^2 / 2{np.round(self.dispersion, 3)})'

        return func

    def three_sigma(self) -> np.ndarray:
        return np.linspace(-3 * self.__dispersion + self.__mu, 3 * self.__dispersion + self.__mu, 100)
    
    def function(self) -> np.ndarray:
        constant = self.__area / np.sqrt(2 * np.pi * np.power(self.__dispersion, 2))
        array = np.exp(-np.power(self.three_sigma() - self.__mu, 2) / (2 * np.power(self.__dispersion, 2)))
        return constant * array
    

class Lorentzian:
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        self.mu = mu
        self.fwhm = fwhm
        self.area = area

    def to_workbook(self) -> str:
        return f'Peak on mu=({self.mu}) with fwhm=({self.fwhm}) and area under peak=({self.area})'

    def __str__(self) -> str:
        func = 'L(x) = '
        func += f'2 * {round(self.area, 3)} / pi'
        func += f'* [{np.round(self.fwhm, 3)} / ((x - {round(self.mu)})^2 + {round(self.fwhm, 3)}^2)]'

        return func
    
    def dispersion(self) -> float:
        return self.fwhm / (2 * np.sqrt(2 * np.log(2)))
    
    def three_sigma(self) -> np.ndarray:
        sigma = self.dispersion()
        return np.linspace(-5 * sigma + self.mu, 5 * sigma + self.mu, 50)
    
    def function(self) -> np.ndarray:
        constant = 2 * self.area / np.pi
        brackets = self.fwhm / (4 * (self.three_sigma() - self.mu) ** 2 + self.fwhm ** 2)

        return constant * brackets


class Peak:
    def __init__(self, spectrum: np.ndarray, mu_index: int, fwhm: int) -> None:
        self.spectrum = spectrum
        self.mu_index = mu_index

        self.width = fwhm / np.log10(2)
        self.area = 0

    def approximate(self) -> Gaussian:
        peak_start = self.mu_index - self.width / 2
        peak_stop = self.mu_index + self.width / 2

        peak_start = int(peak_start) if peak_start >= 0 else 0
        peak_stop = int(peak_stop) if peak_stop < len(self.spectrum) else len(self.spectrum) - 1
        center_index = self.mu_index - peak_stop

        return Peak.describe(np.arange(peak_start, peak_stop), self.spectrum[peak_start: peak_stop], center_index)

    @staticmethod
    def describe(x: np.ndarray, y: np.ndarray, center: int) -> Gaussian:
        new_x = np.power(x - x[center], 2)
        y[y == 0] = 1
        new_y = np.log(y)

        coeffs = Peak.least_squares(new_x, new_y)

        sigma = np.sqrt(-1 / (2 * coeffs[0]))
        area = np.exp(coeffs[1]) * np.sqrt(2 * np.pi * sigma ** 2)

        return Gaussian(x[center], sigma, area)

    @staticmethod
    def least_squares(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
        system = np.array([[len(x), x.sum()], [x.sum(), np.power(x, 2).sum()]])
        righthand = np.array([y.sum(), (x * y).sum()])

        solutions = np.linalg.solve(system, righthand)
        return (solutions[1], solutions[0])


class Spectrum:
    def __init__(self, reaction: Reaction, angle: float, electronics: Telescope, data: list[int]) -> None:
        self.__angle = angle
        self.__reaction = reaction
        self.__electronics = electronics

        self.__data = np.array(data)

        self.__scale_shift = 0
        self.__scale_value = 0

        self.__peaks: dict[float, Gaussian] = dict()

    @property
    def is_calibrated(self) -> bool:
        return len(self.energy_view) != 0
    
    @property
    def gamma_widths(self) -> list[float]:
        self_widths = np.array(self.__reaction.residual.wigner_widths)
        detector_resolution = self.__electronics.e_detector.resolution
        return np.sqrt(self_widths ** 2 + detector_resolution ** 2).tolist()
    
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
    def data(self) -> np.ndarray:
        return self.__data
    
    @property
    def energy_view(self) -> np.ndarray:
        if self.__scale_shift == 0 and self.__scale_value == 0:
            return np.array([])
        
        return self.__scale_value * np.arange(1, len(self.__data) + 1) + self.__scale_shift
    
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
        
        if state not in self.reaction.residual.states:
            raise ValueError(f'There is no state of residual nuclei of reaction same as {state}')
        
        self.__peaks[state] = peak


class SpectrumAnalyzer:
    def __init__(self, spectrums: list[Spectrum]) -> None:
        self.spectrums = spectrums
        self.dsigma = self.__create_cross_section()

    def __create_cross_section(self) -> CrossSection:
        angles = np.array([sp.angle for sp in self.spectrums])
        return CrossSection(self.spectrums[0].reaction, angles)

    def approximate(self, index: int) -> None:
        spectrum = self.spectrums[index]
        if not spectrum.is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')

        states = spectrum.reaction.residual.states

        found = self.find_peaks(index)
        for i in range(len(found)):
            spectrum.add_peak(states[i], found[i].approximate())
            
    def find_peaks(self, index: int) -> list[Peak]:
        spectrum = self.spectrums[index]
        if not spectrum.is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')
        
        theories = self.theory_peaks(index)
        
        collected = []
        for i in range(len(theories)):
            k, e0 = spectrum.scale_value, spectrum.scale_shift

            pretend_channel = int((theories[i] - e0) / k) - 1
            if pretend_channel <= 0:
                continue

            fwhm_in_channels = int(spectrum.gamma_widths[i] / spectrum.scale_value)
            collected.append(Peak(spectrum.data, pretend_channel, fwhm_in_channels))

        return collected
    
    def theory_peaks(self, index: int) -> list[float]:
        current = self.spectrums[index]

        piercing = current.electronics.de_detector
        stopping = current.electronics.e_detector

        de_bete_bloch = Struggling(current.reaction.fragment, piercing.madeof_nuclei)
        e_bete_bloch = Struggling(current.reaction.fragment, stopping.madeof_nuclei)

        likely_peaks = []
        for state in current.reaction.residual.states:
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

        matrix = np.array([[anchors_indexes[0], 1], [anchors_indexes[1], 1]])
        right_side = np.array([theories[first_state_index], theories[second_state_index]])

        solution = np.linalg.solve(matrix, right_side)
        current.scale_value, current.scale_shift = solution[0], solution[1]


if __name__ == '__main__':
    pass
