import numpy as np
from business.parsing import USBParser
from business.physics import Nuclei, Reaction
from business.analysis import Analyzer, Spectrum
from business.electronics import Telescope


class Locus:
    def __init__(self, nuclei: Nuclei, matrix: np.ndarray, points: list[tuple[int, int]]) -> None:
        self.nuclei = nuclei
        self.matrix = matrix
        self.points = points
    
    def cut_locus_shape(self) -> list[list[int]]:
        pass

    def to_spectrum(self) -> list[int]:
        pass


class Matrix:
    def __init__(self, parser: USBParser, electronics: Telescope) -> None:
        self.parser = parser
        self.electronics = electronics

        self.numbers = self.parser.get_matrix()

    @property
    def angle(self) -> float:
        return self.parser.get_angle()

    @property
    def integrator_counts(self) -> int:
        return self.parser.get_integrator_counts()
    
    @property
    def misscalculation(self) -> float:
        return self.parser.get_misscalculation()
    
    def all_spectres(self) -> dict[Nuclei, Spectrum]:
        pass

    def generate_locus_spectrum(self, particle: Nuclei) -> Spectrum:
        locus = next(item for item in self.generate_all_locuses() if item.nuclei == particle)
        return Spectrum(self.__build_reaction(particle), self.angle, self.electronics, locus.to_spectrum())
    
    def generate_all_locuses(self) -> list[Locus]:
        pass
    
    def __build_reaction(self, fragment: Nuclei) -> Reaction:
        beam = self.parser.parse_beam()
        target = self.parser.parse_target()
        energy = self.parser.get_beam_energy()

        return Reaction(beam, target, fragment, energy)


if __name__ == '__main__':
    pass