import numpy as np

from business.decoding import Decoder
from business.locus import Locus
from business.analysis import Spectrum, SpectrumAnalyzer
from business.physics import Nuclei, Reaction


class Matrix:
    def __init__(self, decoder: Decoder) -> None:
        self.decoder = decoder
        self.numbers = decoder.get_matrix()
        self.experiment = decoder.get_experiment()
        self.electronics = decoder.get_electronics()

        self.locuses: list[Locus] = decoder.take_locuses()
        self.spectrums: list[Spectrum] = decoder.take_spectrums()

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
        if particle in [locus.particle for locus in self.locuses]:
            index = next(i for i in range(len(self.locuses)) if self.locuses[i].particle == particle)
            self.locuses[index] = Locus(particle, self.numbers, points)
        else:
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
    

# TODO: Refactor and implement that class.
class MatrixAnalyzer:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self.matrixes = matrixes

    @property
    def angles(self) -> list[float]:
        return [matrix.angle for matrix in self.matrixes]
    
    def all_spectres(self) -> list[SpectrumAnalyzer]:
        particles = []
        for m in self.matrixes:
            for locus in m.locuses:
                if locus.particle not in particles:
                    particles.append(locus.particle)

        return [self.collect_spectres(p) for p in particles]

    def collect_spectres(self, particle: Nuclei) -> SpectrumAnalyzer:
        return SpectrumAnalyzer([m.spectrum_of(particle) for m in self.matrixes])

    def cross_section_of(self, particle: Nuclei) -> np.ndarray:
        pass


if __name__ == '__main__':
    pass
