import numpy as np

from business.decoding import Decoder
from business.locus import Locus
from business.usb2ds import USBParser
from business.analysis import Spectrum
from business.yard import NucleiConverter
from business.physics import Nuclei, Reaction


class Demo:
    def __init__(self, parser: USBParser) -> None:
        self.parser = parser
        self.numbers = self.parser.get_matrix()

    @property
    def angle(self) -> float:
        return self.parser.get_angle()

    @property
    def integrator_counts(self) -> int:
        return self.parser.get_integrator_counts()
    
    @property
    def integrator_constant(self) -> int:
        return self.parser.get_integrator_constant()
    
    @property
    def misscalculation(self) -> float:
        return self.parser.get_misscalculation()
    
    def to_workbook(self) -> str:
        beam = NucleiConverter.to_string(self.parser.parse_beam())
        target = NucleiConverter.to_string(self.parser.parse_target())

        report = f'Matrix {self.parser.matrix_sizes} of -> \n'
        report += f'{target} + {beam} reaction at {self.parser.parse_beam_energy()} MeV.\n'
        report += f"Telescope's angle in lab-system: {self.angle} degrees.\n"
        report += f"Integrator's count: {self.integrator_counts}\n"
        report += f"Integrator's module constant: {self.integrator_constant} Coul/pulse.\n"
        report += f"Telescope's efficiency: {self.misscalculation}.\n"

        locuses = self.parser.take_locuses()
        for nuclei in locuses:
            report += f'Locus of {NucleiConverter.to_string(nuclei)}:\n'
            for i in locuses[nuclei]:
                report += f'\t(E: {i[0]}; dE: {i[1]})\n'

        return report

    def spectrums(self) -> list[list[int]]:
        alls = self.locuses()
        return [each.to_spectrum() for each in alls]
    
    def locuses(self) -> list[Locus]:
        alls = self.parser.take_locuses()
        return [Locus(each, self.numbers, alls[each]) for each in alls]
    

class Matrix:
    def __init__(self, decoder: Decoder) -> None:
        self.decoder = decoder
        self.numbers = decoder.get_matrix()
        self.experiment = decoder.get_experiment()
        self.electronics = decoder.get_electronics()

        self.locuses: list[Locus] = []
        self.spectrums: list[Spectrum] = []

    @property
    def angle(self) -> float:
        return self.decoder.get_angle()
    
    @property
    def integrator_counts(self) -> int:
        return self.decoder.get_integrator_counts()
    
    @property
    def integrator_constant(self) -> float:
        return self.decoder.get_integrator_constant()
    
    @property
    def misscalculation(self) -> float:
        return self.decoder.get_misscalculation()

    def add_locus(self, particle: Nuclei, points: list[tuple[int, int]]) -> None:
        self.locuses.append(Locus(particle, self.numbers, points))

    def spectrum_of(self, particle: Nuclei) -> Spectrum:
        if particle not in [locus.particle for locus in self.locuses]:
            raise ValueError(f'There is no locus of {particle} in matrix.')
        
        locus = next(locus for locus in self.locuses if locus.particle == particle)
        reaction = self.__build_reaction(particle)
        spectrum_data = locus.to_spectrum()

        self.spectrums.append(Spectrum(reaction, self.angle, self.electronics, spectrum_data))
        return self.spectrums[-1]

    def __build_reaction(self, fragment: Nuclei) -> Reaction:
        return self.experiment.create_reaction(fragment)
    

class MatrixAnalyzer:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self.matrixes = matrixes

    def collect_spectres(self, particle: Nuclei) -> list[Spectrum]:
        pass

    def cross_section_of(self, particle: Nuclei) -> np.ndarray:
        pass


if __name__ == '__main__':
    pass
