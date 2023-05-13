import numpy as np
from business.maths import *
from business.physics import Reaction


class Spectrum:
    PEAKS_LENGTH = 10

    def __init__(self, reaction: Reaction, angle: float, integrator: int, misscalculation: float, data: list[int]) -> None:
        self.reaction = reaction

        self.angle = reaction.fragment_angle
        self.integrator = integrator
        self.misscalculation = misscalculation

        self.data = np.array(data)

    def find_anchor_peaks(self) -> list[int]:
        first_peak = self.data.argmax()
        second_peak = np.hstack([
            self.data[:first_peak - self.PEAKS_LENGTH // 2], 
            self.data[first_peak + self.PEAKS_LENGTH // 2 + 1:]
            ]).argmax()

        first_peak += 1
        if second_peak >= first_peak:
            second_peak += self.PEAKS_LENGTH + 2
        else:
            second_peak += 1

        return [first_peak, second_peak]


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
        temp_data = self.spectrum.data[:self.ending_channel] - self.parabola.values(np.arange(self.ending_channel) * self.calib_coeff + self.calib_e0)
        self.cutted_data = np.hstack((temp_data, self.spectrum.data[self.ending_channel + 1:]))


class Analyzer:
    def __init__(self, spectrum: Spectrum, states: list[float], gamma_widths: list[float]) -> None:
        self.spectrum = spectrum

        self.states = states
        self.theory_peaks = [spectrum.reaction.fragment_energy(state) for state in states]
        self.gamma_widths = gamma_widths

        self.calibrator = Calibrator(spectrum)
        self.cutter = Cutter(spectrum)

        self._is_calibrated = False
        self._is_cutted = False

        self.events: list[float] = list()
        self.gaussians: list[Gaussian] = list()

    def calibrate_spectrum(self) -> None:
        peak_indexes = self.spectrum.find_anchor_peaks()
        self.calibrator.calibrate(peak_indexes)

        self._is_calibrated = True

    def cut_spectrum(self) -> None:
        if not self._is_calibrated:
            self.calibrate_spectrum()
        
        anchors = np.array(self.spectrum.find_anchor_peaks())
        last_peak = anchors[anchors.argmin()]
        
        self.cutter.cut(self.calibrator.scale_value, self.calibrator.scale_shift, last_peak)
        self._is_cutted = True

    def change_cut(self, val: float) -> None:
        if not self._is_calibrated:
            self.calibrate_spectrum()

        if not self._is_cutted:
            self.cut_spectrum()
        
        if val == 0:
            return
        
        self.cutter.change_cut(val)

    def find_peaks(self) -> list[int]:
        if not self._is_calibrated:
            self.calibrate_spectrum()
        
        collected = []
        for peak in self.theory_peaks:
            pretend_channel = int((peak - self.calibrator.scale_shift) / self.calibrator.scale_value)
            if pretend_channel <= 5:
                continue
            
            index_ranges = (pretend_channel - self.spectrum.PEAKS_LENGTH // 2, pretend_channel + self.spectrum.PEAKS_LENGTH // 2 + 1)
            all_peak = self.cutter.cutted_data[index_ranges[0]: index_ranges[1]]

            center = all_peak.argmax() + pretend_channel - self.spectrum.PEAKS_LENGTH // 2
            if center not in collected:
                collected.append(center)

        return collected

    def approximate(self) -> None:
        if not self._is_calibrated:
            self.calibrate_spectrum()

        if not self._is_cutted:
            self.cut_spectrum()

        peaks = self.find_peaks()
        for i in range(len(peaks)):
            index_ranges = (peaks[i] - self.spectrum.PEAKS_LENGTH // 2, peaks[i] + self.spectrum.PEAKS_LENGTH // 2 + 1)

            peak_x = self.calibrator.energy_view[index_ranges[0]: index_ranges[1]]
            peak_y = self.cutter.cutted_data[index_ranges[0]: index_ranges[1]]

            self.gaussians.append(Gaussian(np.array([peak_x, peak_y]), self.gamma_widths[i]))
            self.events.append(self.gaussians[-1].area)

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
