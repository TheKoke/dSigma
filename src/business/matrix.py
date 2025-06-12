import numpy

from business.locus import Locus
from business.decoding import Decoder
from business.analysis import Spectrum, SpectrumAnalyzer
from business.physics import Nuclei, Reaction, CrossSection


class Matrix:
    def __init__(self, decoder: Decoder) -> None:
        self.decoder = decoder
        self.numbers = decoder.get_matrix()
        self.experiment = decoder.get_experiment()
        self.electronics = decoder.get_electronics()

        self.angle = decoder.get_angle()
        self.integrator_counts = decoder.get_integrator_counts()
        self.integrator_constant = decoder.get_integrator_constant()
        self.misscalculation = decoder.get_misscalculation()

        self.locuses: dict[Nuclei, Locus] = decoder.take_locuses()
        self.spectrums: dict[Nuclei, Spectrum] = decoder.take_spectrums()
    
    def to_workbook(self) -> str:
        beam = self.experiment.beam
        target = self.experiment.target

        report = f'Matrix {self.decoder.matrix_sizes} of -> \n'
        report += f'{target} + {beam} reaction at {self.experiment.beam_energy} MeV.\n'
        report += f"Telescope's angle in lab-system: {self.angle} degrees.\n"
        report += f"Integrator's count: {self.integrator_counts}\n"
        report += f"Integrator's module constant: {self.integrator_constant} Coul/pulse.\n"
        report += f"Telescope's efficiency: {self.misscalculation}.\n"
        report += f"dE detector thickness: {self.electronics.de_detector.thickness} micron.\n"
        report += f"E detector thickness: {self.electronics.e_detector.thickness} micron.\n"

        report += '\n\n'
        for nuclei in self.locuses:
            report += f'Locus of {nuclei.name}:\n'
            report += self.locuses[nuclei].to_workbook()
            report += '--\n'

        report += '\nSpectrum area\n'
        for nuclei in self.spectrums:
            report += self.spectrums[nuclei].to_workbook()
            report += '--\n'

        return report

    def add_locus(self, particle: Nuclei, points: list[tuple[int, int]]) -> None:
        self.locuses[particle] = Locus(self.numbers, points)
        
        reaction = self.__build_reaction(particle)
        spectrum_data = self.locuses[particle].to_spectrum()
        self.spectrums[particle] = Spectrum(reaction, self.angle, self.electronics, spectrum_data)

    def spectrum_of(self, particle: Nuclei) -> Spectrum:
        if particle in [self.spectrums[n].reaction.fragment for n in self.spectrums]:
            return next(self.spectrums[n] for n in self.spectrums if self.spectrums[n].reaction.fragment == particle)

        if particle in self.locuses:
            locus = self.locuses[particle]
            reaction = self.__build_reaction(particle)
            spectrum_data = locus.to_spectrum()

            self.spectrums[particle] = Spectrum(reaction, self.angle, self.electronics, spectrum_data)
            return self.spectrums[particle]
        
        raise ValueError(f'There is no spectrum of {particle} fragment.')

    def __build_reaction(self, fragment: Nuclei) -> Reaction:
        return self.experiment.create_reaction(fragment)


if __name__ == '__main__':
    pass
