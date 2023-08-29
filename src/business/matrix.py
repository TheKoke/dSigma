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

        self.locuses: list[Locus] = decoder.take_locuses()
        self.spectrums: dict[Nuclei, Spectrum] = decoder.take_spectrums()

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
        for locus in self.locuses:
            report += f'Locus of {locus.particle.name}:\n'
            for i in locus.points:
                report += f'\t(E: {i[0]}; dE: {i[1]})\n'
            report += '--\n'

        report += '\nSpectrum area\n'
        for nuclei in self.spectrums:
            report += self.spectrums[nuclei].to_workbook()
            report += '--\n'

        return report

    def add_locus(self, particle: Nuclei, points: list[tuple[int, int]]) -> None:
        if particle in [locus.particle for locus in self.locuses]:
            index = next(i for i in range(len(self.locuses)) if self.locuses[i].particle == particle)
            self.locuses[index] = Locus(particle, self.numbers, points)

            self.spectrums.pop(particle)
        else:
            self.locuses.append(Locus(particle, self.numbers, points))

    def spectrum_of(self, particle: Nuclei) -> Spectrum:
        if particle in [self.spectrums[n].reaction.fragment for n in self.spectrums]:
            return next(self.spectrums[n] for n in self.spectrums if self.spectrums[n].reaction.fragment == particle)

        if particle in [locus.particle for locus in self.locuses]:
            locus = next(locus for locus in self.locuses if locus.particle == particle)
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
        self.analyzers = self.__all_analyzers()

    @property
    def angles(self) -> list[float]:
        return [matrix.angle for matrix in self.matrixes]
    
    def __all_analyzers(self) -> list[SpectrumAnalyzer]:
        particles = self.__particles()
        return [self.__collect_spectres(p) for p in particles]

    def __collect_spectres(self, particle: Nuclei) -> SpectrumAnalyzer:
        return SpectrumAnalyzer([m.spectrum_of(particle) for m in self.matrixes])
    
    def __particles(self) -> list[Nuclei]:
        found = []
        for m in self.matrixes:
            for locus in m.locuses:
                if locus.particle not in found:
                    found.append(locus.particle)

        return found
    
    def all_dsigmas(self) -> list[CrossSection]:
        voids = [sp.dsigma for sp in self.analyzers]

        for ds in voids:
            current_particle = ds.reaction.fragment
            current_residual_states = ds.reaction.residual.states

            for state in current_residual_states:
                ds.add_cross_section_for(state, self.cross_section_of(current_particle, state))

        return voids

    def cross_section_of(self, particle: Nuclei, state: float) -> np.ndarray:
        fragments = self.__particles()
        if particle not in fragments:
            raise ValueError(f'{particle} fragment does not exist.')
        
        splitted = self.__split_by_telescope()

        cs = []
        for bunch in splitted:
            events = []
            integrator = []
            misscalc = []

            for matrix in bunch:
                if state in matrix.spectrums[particle].peaks:
                    integrator.append(matrix.integrator_counts)
                    misscalc.append(matrix.misscalculation)
                    events.append(matrix.spectrums[particle].peaks[state].area)

            events = np.array(events)
            integrator = np.array(integrator)
            misscalc = np.array(misscalc)

            cs.append(self.__formula(events, integrator, misscalc, bunch[0].electronics))

        return cs
        
    def __split_by_telescope(self) -> list[list[Matrix]]:
        collected = []
        current = None

        for matrix in self.matrixes:
            if current is None:
                current = matrix.electronics
                collected.append([matrix])
                continue

            if matrix.electronics == current:
                collected[-1].append(matrix)
            else:
                current = None

        return collected

    @staticmethod
    def __formula(events: np.ndarray, integrator: np.ndarray, misscalculation: np.ndarray, telescope: Telescope) -> np.ndarray:
        numerator =  events * misscalculation
        denumerator = integrator * telescope.integrator_constant * MatrixAnalyzer.__solid_angle(telescope)

        return numerator / denumerator

    @staticmethod
    def __solid_angle(telescope: Telescope) -> float:
        return 2 * np.pi * (telescope.collimator_radius ** 2) / (telescope.distance ** 2)


if __name__ == '__main__':
    pass
