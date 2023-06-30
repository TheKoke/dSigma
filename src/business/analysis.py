import numpy as np
from business.maths import *
from business.physics import Reaction


class Spectrum:
    def __init__(self, reaction: Reaction, angle: float, integrator: int, misscalculation: float, data: list[int]) -> None:
        self.reaction = reaction

        self.angle = angle
        self.integrator = integrator
        self.misscalculation = misscalculation

        self.data = np.array(data)


class Calibrator:
    def __init__(self, spectrum: Spectrum) -> None:
        self.spectrum = spectrum

        self.scale_shift = 0
        self.scale_value = 0

        self.energy_view = np.array([])

    def calibrate(self, anchors_indexes: list[int], theory_peaks: list[float]) -> None:
        anchors_indexes = sorted(anchors_indexes, reverse=True)

        matrix = np.array([[anchors_indexes[0], 1], [anchors_indexes[1], 1]])
        right_side = np.array([theory_peaks[0], theory_peaks[1]])

        solution = np.linalg.solve(matrix, right_side)

        self.scale_value, self.scale_shift = solution[0], solution[1]
        self.energy_view = np.arange(1, len(self.spectrum.data)) * self.scale_value + self.scale_shift


class Cutter:
    def __init__(self, spectrum: Spectrum) -> None:
        self.spectrum = spectrum

        self.ending_channel = 0
        self.calib_coeff = 0
        self.calib_e0 = 0

        self.cutted_data = np.ndarray([])
        self.parabola = Parabola(0, 0)

    def cut(self, calib_coeff: float, calib_e0: float, ending_channel: int) -> None:
        self.ending_channel = ending_channel
        self.calib_coeff = calib_coeff
        self.calib_e0 = calib_e0

        background_props = self.__define_background()
         
        slope = background_props[0] / np.sqrt(background_props[1] - calib_e0)
        self.parabola = Parabola(slope, background_props[1])

        self.__subract_background()

    def change_cut(self, val: float) -> None:
        self.parabola = Parabola(self.parabola.slope + val, self.parabola.shift)
        self.__subract_background()

    def __define_background(self) -> tuple[float, float]:
        mean = self.spectrum.data[:self.ending_channel + 1].mean()
        return (mean, self.ending_channel * self.calib_coeff + self.calib_e0)

    def __subract_background(self) -> np.ndarray:
        temp_data = self.spectrum.data[:self.ending_channel] - \
            self.parabola.values(np.arange(self.ending_channel) * self.calib_coeff + self.calib_e0)
        self.cutted_data = np.hstack((temp_data, self.spectrum.data[self.ending_channel + 1:]))


class Analyzer:
    def __init__(self, spectrum: Spectrum, states: list[float]) -> None:
        self.spectrum = spectrum

        self.theory_peaks = [spectrum.reaction.fragment_energy(state, self.spectrum.angle) for state in states]
        self.gamma_widths = self.spectrum.reaction.residual.wigner_widths

        self.calibrator = Calibrator(spectrum)
        self._is_calibrated = False

        self.events: list[float] = list()
        self.gaussians: list[Gaussian] = list()

    def calibrate_spectrum(self, peak_indexes: list[int]) -> None:
        self.calibrator.calibrate(peak_indexes, self.theory_peaks)
        self._is_calibrated = True

    def find_peaks(self) -> list[int]:
        if not self._is_calibrated:
            self.calibrate_spectrum()
        
        collected = []
        for peak in self.theory_peaks:
            pretend_channel = int((peak - self.calibrator.scale_shift) / self.calibrator.scale_value)
            if pretend_channel <= 0:
                continue

        return collected

    def approximate(self) -> None:
        if not self._is_calibrated:
            self.calibrate_spectrum()

        peaks = self.find_peaks()
        for i in range(len(peaks)):
            pass

    def change_gaussian(self, index: int, parameter: str, val: float) -> None:
        if index >= len(self.gaussians) or index <= 0:
            return
        
        if parameter == 'center':
            self.gaussians[index].peak_center += val

        if parameter == 'area':
            self.gaussians[index].area += val

        if parameter == 'fwhm':
            self.gaussians[index].fwhm += val


if __name__ == '__main__':
    pass
