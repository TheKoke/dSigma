import numpy

from business.analysis import Spectrum
from business.physics import Reaction, Nuclei


class ImpurityMaster:
    def __init__(self, spectrums: list[Spectrum], suspects: list[Reaction], elastic_spectrums: list[Spectrum]) -> None:
        self.spectres = spectrums
        self.suspects = suspects
        self.elastic = elastic_spectrums

    def handle_impurities(self) -> list[Spectrum]:
        pass

    def define_proportions(self) -> numpy.ndarray:
        if self.spectres[0].reaction == self.elastic[0].reaction:
            return self.spectres[0].reaction.rutherford_scattering()


if __name__ == '__main__':
    pass
