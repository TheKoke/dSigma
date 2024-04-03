import numpy as np

from business.locus import Locus
from business.decoding import Decoder
from business.electronics import Telescope
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


class MatrixAnalyzer:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self.matrixes = matrixes

    @property
    def analyzers(self) -> list[SpectrumAnalyzer]:
        return self.__all_analyzers()

    @property
    def angles(self) -> list[float]:
        return [matrix.angle for matrix in self.matrixes]
    
    def matrix_of_angle(self, angle: float) -> None:
        try:
            return next(matrix for matrix in self.matrixes if matrix.angle == angle)
        except:
            raise ValueError('No such matrix!')
    
    def __all_analyzers(self) -> list[SpectrumAnalyzer]:
        particles = self.__particles()
        return [self.__collect_spectres(p) for p in particles]

    def __collect_spectres(self, particle: Nuclei) -> SpectrumAnalyzer:
        return SpectrumAnalyzer([m.spectrum_of(particle) for m in self.matrixes])
    
    def __particles(self) -> list[Nuclei]:
        found = []
        for m in self.matrixes:
            for nuclei in m.locuses:
                if nuclei not in found:
                    found.append(nuclei)

        return found
    
    def all_dsigmas(self) -> list[CrossSection]:
        voids = [sp.dsigma for sp in self.analyzers]

        for ds in voids:
            current_particle = ds.reaction.fragment
            current_residual_states = ds.reaction.residual_states

            for state in current_residual_states:
                ds.add_cross_section_for(state, self.cross_section_of(current_particle, state))

        return voids

    def cross_section_of(self, particle: Nuclei, state: float) -> np.ndarray:
        fragments = self.__particles()
        if particle not in fragments:
            raise ValueError(f'{particle} fragment does not exist.')
        
        events = []
        integrator = []
        misscalc = []
        intconst = []
        solid_angle = []

        for matrix in self.matrixes:
            if state in matrix.spectrums[particle].peaks:
                solid_angle.append(matrix.electronics.solid_angle())
                intconst.append(matrix.integrator_constant)
                integrator.append(matrix.integrator_counts)
                misscalc.append(matrix.misscalculation)
                events.append(matrix.spectrums[particle].peaks[state].area)

        events = np.array(events)
        integrator = np.array(integrator)
        misscalc = np.array(misscalc)
        intconst = np.array(intconst)
        solid_angle = np.array(solid_angle)

        return self.__relation(events, integrator, misscalc, intconst, solid_angle)

    @staticmethod
    def __relation(events: np.ndarray, integrator: np.ndarray, 
                  misscalculation: np.ndarray, intconstant: np.ndarray,
                  solid_angle: np.ndarray) -> np.ndarray:
        
        numerator =  events * misscalculation
        denumerator = integrator * intconstant * solid_angle

        return numerator / denumerator


if __name__ == '__main__':
    pass
