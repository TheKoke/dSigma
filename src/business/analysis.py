import numpy
from business.electronics import Telescope
from business.peaks import PeakAnalyzer, PeakFunction
from business.physics import Reaction, CrossSection, Struggling


class Spectrum:
    def __init__(self, reaction: Reaction, angle: float, electronics: Telescope, data: list[int]) -> None:
        self.__angle = angle
        self.__reaction = reaction
        self.__electronics = electronics

        self.__data = numpy.array(data)

        self.__scale_shift = 0
        self.__scale_value = 0

        self.__peaks: dict[float, PeakFunction] = dict()

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
    def peaks(self) -> dict[float, PeakFunction]:
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
    
    def add_peak(self, state: float, peak: PeakFunction) -> None:
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
        return CrossSection(self.spectrums[0].reaction)
    
    def angles(self) -> list[float]:
        return [sp.angle for sp in self.spectrums]

    def approximate(self, index: int) -> None:
        spectrum = self.spectrums[index]
        if not spectrum.is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')

        states = spectrum.reaction.residual_states

        found = self.find_peaks(index)
        for i in range(len(found)):
            peak = found[i].approximate()
            if numpy.isnan(peak.area) or numpy.isnan(peak.fwhm):
                continue

            if numpy.isinf(peak.area) or numpy.isinf(peak.fwhm):
                continue

            spectrum.add_peak(states[i], peak)
            
    def find_peaks(self, index: int) -> list[PeakAnalyzer]:
        spectrum = self.spectrums[index]
        if not spectrum.is_calibrated:
            raise ValueError('Spectrum must be calibrated before finding peaks')
        
        theories = self.theory_peaks(index)

        e_detector = spectrum.electronics.e_detector
        de_detector = spectrum.electronics.de_detector

        e_detector_thick = e_detector.thickness * 10e-6
        de_detector_thick = de_detector.thickness * 10e-6

        de_bete_bloch = Struggling(spectrum.reaction.fragment, de_detector.madeof_nuclei)
        e_bete_bloch = Struggling(spectrum.reaction.fragment, e_detector.madeof_nuclei)

        collected = []
        for i in range(len(theories)):
            k, e0 = spectrum.scale_value, spectrum.scale_shift

            de_loss = de_bete_bloch.energy_loss(theories[i], de_detector_thick, de_detector.density)
            remain_energy = theories[i] - de_loss

            e_loss = e_bete_bloch.energy_loss(remain_energy, e_detector_thick, e_detector.density)
            remain_energy -= e_loss

            if remain_energy <= 0:
                continue

            pretend_channel = int((remain_energy - e0) / k)
            if pretend_channel <= len(self.spectrums[index].data) * 0.02:
                continue

            collected.append(PeakAnalyzer(spectrum.data, pretend_channel))

        return collected
    
    def theory_peaks(self, index: int) -> list[float]:
        current = self.spectrums[index]

        peaks = []
        for state in current.reaction.residual_states:
            fragment_energy = current.reaction.fragment_energy(state, current.angle)
            if numpy.isnan(fragment_energy) or numpy.isinf(fragment_energy):
                break

            peaks.append(fragment_energy)

        return peaks
    
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
