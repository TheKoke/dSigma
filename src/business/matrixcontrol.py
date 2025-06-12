import numpy

from business.matrix import Matrix
from business.encoding import Encoder
from business.analysis import SpectrumAnalyzer
from business.physics import Nuclei, CrossSection


class MatrixAnalyzer:
    def __init__(self, matrixes: list[Matrix]) -> None:
        self.__matrixes = sorted(matrixes, key=lambda x: x.angle)

    @property
    def matrixes(self) -> list[Matrix]:
        return self.__matrixes.copy()

    @property
    def analyzers(self) -> list[SpectrumAnalyzer]:
        return self.__all_analyzers()

    @property
    def angles(self) -> list[float]:
        return [matrix.angle for matrix in self.__matrixes]
    
    def __all_analyzers(self) -> list[SpectrumAnalyzer]:
        particles = self.__particles()
        return [self.__collect_spectres(p) for p in particles]

    def __collect_spectres(self, particle: Nuclei) -> SpectrumAnalyzer:
        return SpectrumAnalyzer([m.spectrum_of(particle) for m in self.__matrixes])
    
    def __particles(self) -> list[Nuclei]:
        found = []
        for m in self.__matrixes:
            for nuclei in m.locuses:
                if nuclei not in found:
                    found.append(nuclei)

        return found
    
    def join_matrixes(self, index1: int, index2: int) -> None:
        first = self.__matrixes.pop(index1)
        second = self.__matrixes.pop(index2)

        joiner = MatrixJoiner(first, second)
        self.__matrixes.append(joiner.join())
    
    def all_dsigmas(self) -> list[CrossSection]:
        voids = [sp.dsigma for sp in self.analyzers]

        for ds in voids:
            current_particle = ds.reaction.fragment
            current_residual_states = ds.reaction.residual_states

            for state in current_residual_states:
                ds.add_cross_section_for(state, *self.cross_section_of(current_particle, state))

        return voids

    def cross_section_of(self, particle: Nuclei, state: float) -> tuple[numpy.ndarray, numpy.ndarray]:
        fragments = self.__particles()
        if particle not in fragments:
            raise ValueError(f'{particle} fragment does not exist.')
        
        angles = []
        events = []
        integrator = []
        misscalc = []
        intconst = []
        solid_angle = []

        for matrix in self.__matrixes:
            if state in matrix.spectrums[particle].peaks:
                solid_angle.append(matrix.electronics.solid_angle())
                intconst.append(matrix.integrator_constant)
                integrator.append(matrix.integrator_counts)
                misscalc.append(matrix.misscalculation)
                events.append(matrix.spectrums[particle].peaks[state].area)
                angles.append(matrix.angle)

        angles = numpy.array(angles)
        events = numpy.array(events)
        integrator = numpy.array(integrator)
        misscalc = numpy.array(misscalc)
        intconst = numpy.array(intconst)
        solid_angle = numpy.array(solid_angle)

        return (angles, self.__relation(events, integrator, misscalc, intconst, solid_angle))

    @staticmethod
    def __relation(events: numpy.ndarray, integrator: numpy.ndarray, 
                  misscalculation: numpy.ndarray, intconstant: numpy.ndarray,
                  solid_angle: numpy.ndarray) -> numpy.ndarray:
        
        numerator =  events * misscalculation
        denumerator = integrator * intconstant * solid_angle

        return numerator / denumerator
    

class MatrixJoiner:
    def __init__(self, matrix1: Matrix, matrix2: Matrix, is_first_main: bool = True) -> None:
        self.first = matrix1
        self.second = matrix2
        self.is_first_main = is_first_main

    def join(self) -> Matrix:
        if not (self.compare_physics() and self.compare_electronics()):
            raise ValueError('The matrixes hasn\'t same conditions to be joined.')
        
        new_numbers = self.first.numbers + self.second.numbers
        new_integrator = self.first.integrator_counts + self.second.integrator_constant
        new_coincidence = int(self.first.misscalculation * self.first.numbers.sum()) + int(self.second.misscalculation * self.second.numbers.sum())

        copy = Matrix(self.first.decoder if self.is_first_main else self.second.decoder)
        copy.numbers = new_numbers
        copy.integrator_counts = new_integrator
        copy.misscalculation = new_coincidence / new_numbers.sum()

        return copy

    def compare_physics(self) -> bool:
        is_comparable = self.first.angle == self.second.angle
        is_comparable = is_comparable and self.first.experiment.beam == self.second.experiment.beam
        is_comparable = is_comparable and self.first.experiment.target == self.second.experiment.target
        is_comparable = is_comparable and self.first.experiment.beam_energy == self.second.experiment.beam_energy

        return is_comparable

    def compare_electronics(self) -> bool:
        is_comparable = self.first.integrator_constant == self.second.integrator_constant
        is_comparable = is_comparable and self.first.electronics.de_detector == self.second.electronics.de_detector
        is_comparable = is_comparable and self.first.electronics.e_detector == self.second.electronics.e_detector
        is_comparable = is_comparable and self.first.electronics.solid_angle() == self.second.electronics.solid_angle()

        return is_comparable
    

if __name__ == '__main__':
    pass