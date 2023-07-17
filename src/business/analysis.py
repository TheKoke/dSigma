import numpy as np
from business.physics import Reaction, Struggling
from business.electronics import Telescope


class Gaussian:
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        self.mu = mu
        self.fwhm = fwhm
        self.area = area

    def to_workbook(self) -> str:
        return f'Peak on mu=({self.mu}) with fwhm=({self.fwhm}) and area under peak=({self.area})'

    def __str__(self) -> str:
        func = 'G(x) = '
        func += f'{np.round(self.area, 3)} / (sqrt(2pi * {np.round(self.dispersion(), 3)}) * '
        func += f'exp(-(x - {np.round(self.mu, 3)})^2 / 2{np.round(self.dispersion(), 3)})'

        return func

    def dispersion(self) -> np.float64:
        return self.fwhm / (2 * np.sqrt(2 * np.log(2)))

    def three_sigma(self) -> np.ndarray:
        sigma = self.dispersion()
        return np.linspace(-3 * sigma + self.mu, 3 * sigma + self.mu, 50)

    def function(self) -> np.ndarray:
        constant = self.area / (self.fwhm * np.sqrt(np.pi / (4 * np.log(2))))
        exp_constant = -1 * (4 * np.log(2)) / (self.fwhm ** 2)

        array_part = (self.three_sigma() - self.mu) ** 2
        return constant * np.exp(exp_constant * array_part)
    

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


class Spectrum:
    def __init__(self, reaction: Reaction, angle: float, electronics: Telescope, data: list[int]) -> None:
        self.angle = angle
        self.reaction = reaction
        self.electronics = electronics

        self.data = np.array(data)

        self.scale_shift = 0
        self.scale_value = 0

        self.energy_view = np.array([])

    @property
    def is_calibrated(self) -> bool:
        return len(self.energy_view) != 0
    
    @property
    def gamma_widths(self) -> list[float]:
        self_widths = np.array(self.reaction.residual.wigner_widths)

        detector_resolution = self.electronics.e_detector.resolution
        beam_energy_emittance = self.reaction.beam_energy * 0.01 # cyclotrone u-150m
        environment_resolution = np.sqrt(detector_resolution ** 2 + beam_energy_emittance ** 2)

        return np.sqrt(self_widths ** 2 + environment_resolution ** 2).tolist()

    def theory_peaks(self) -> list[float]:
        piercing = self.electronics.de_detector
        stopping = self.electronics.e_detector

        de_bete_bloch = Struggling(self.reaction.fragment, piercing.madeof_nuclei)
        e_bete_bloch = Struggling(self.reaction.fragment, stopping.madeof_nuclei)

        likely_peaks = []
        for state in self.reaction.residual.states:
            initial = self.reaction.fragment_energy(state, self.angle)

            de_loss = de_bete_bloch.energy_loss(initial, piercing.thickness, piercing.density)
            if initial < de_loss:
                break

            e_loss = e_bete_bloch.energy_loss(initial - de_loss, stopping.thickness, stopping.density)
            if initial - de_loss < e_loss:
                likely_peaks.append(initial - de_loss)
            else:
                likely_peaks.append(e_loss)

        return likely_peaks

    def calibrate(self, anchors_indexes: list[int]) -> tuple[float, float]:
        anchors_indexes = sorted(anchors_indexes, reverse=True)
        theory_peaks = self.theory_peaks()

        matrix = np.array([[anchors_indexes[0], 1], [anchors_indexes[1], 1]])
        right_side = np.array([theory_peaks[0], theory_peaks[1]])

        solution = np.linalg.solve(matrix, right_side)

        self.scale_value, self.scale_shift = solution[0], solution[1]
        self.energy_view = np.arange(1, len(self.data)) * self.scale_value + self.scale_shift

        return (self.scale_value, self.scale_shift)


class Peak:
    def __init__(self, spectrum: np.ndarray, mu_index: int, fwhm: int) -> None:
        self.spectrum = spectrum
        self.mu_index = mu_index
        self.width = fwhm / np.log10(2)

        self.fwhm = fwhm
        self.area = 0

    def approximate(self) -> Gaussian:
        peak_start = self.mu_index - self.width() // 2
        peak_stop = self.mu_index + self.width() // 2

        peak_start = peak_start if peak_start >= 0 else 0
        peak_stop - peak_stop if peak_stop < len(self.spectrum) else len(self.spectrum) - 1

        mu = self.mu_index + 1
        area = self.tuck_up_area(np.arange(peak_start, peak_stop), self.spectrum[peak_start: peak_stop])

        return Gaussian(mu, self.fwhm, area)

    def tuck_up_area(self, xdata: np.ndarray, ydata: np.ndarray) -> float:
        sigma = self.fwhm / (2 * np.sqrt(2 * np.log(2)))
        mu = self.mu_index + 1

        xs = 1 / np.sqrt(2 * np.pi * sigma ** 2) * np.exp(- (xdata - mu) ** 2 / (2 * sigma ** 2))
        return (ydata * xs).sum() / (xs ** 2).sum()


class Analyzer:
    def __init__(self, spectrums: list[Spectrum]) -> None:
        self.spectrums = spectrums

        self.events: list[list[float]] = [0] * len(self.spectrums)
        self.gaussians: list[list[Gaussian]] = [0] * len(spectrums)

    def to_workbook(self, index: int) -> str:
        report = f'{self.spectrums[index].angle} degree spectrum analysis.\n'

        report += f'Spectrum was calibrated by:'
        report += f' E(ch) = {round(self.spectrums[index].scale_value, 3)}*ch + {round(self.spectrums[index].scale_shift)}\n'

        report += 'Peaks analysis info:\n'
        for peak in self.gaussians[index]:
            report += '\t' + peak.to_workbook() + '\n'

        report += '\n\n'
        return report

    def approximate(self, index: int) -> None:
        if not self.spectrums[index].is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')

        self.gaussians[index] = list()
        self.events[index] = list()

        peaks = self.find_peaks(index)
        for peak in peaks:
            curr = peak.approximate()
            self.gaussians[index].append(curr)
            self.events[index].append(curr.area)
            
    def find_peaks(self, index: int) -> list[Peak]:
        if not self.spectrums[index].is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')
        
        theories = self.spectrums[index].theory_peaks()
        
        collected = []
        for i in range(len(theories)):
            k, e0 = self.spectrums[index].scale_value, self.spectrums[index].scale_shift

            pretend_channel = int((theories[i] - e0) / k) - 1
            if pretend_channel <= 0:
                continue

            fwhm_in_channels = int(self.spectrums[index].gamma_widths[i] / self.spectrums[index].scale_value)
            collected.append(Peak(self.spectrums[index], pretend_channel, fwhm_in_channels))

        return collected

    def calibrate_spectrum(self, index: int, peak_indexes: list[int]) -> tuple[float, float]:
        return self.spectrums[index].calibrate(peak_indexes)


if __name__ == '__main__':
    pass
