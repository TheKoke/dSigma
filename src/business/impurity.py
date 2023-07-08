import numpy as np

from business.analysis import Spectrum
from business.physics import Reaction, Nuclei


class ImpurityMaster:
    def __init__(self, spectrums: list[Spectrum], suspects: list[Reaction]) -> None:
        self.spectres = spectrums
        self.suspects = suspects


if __name__ == '__main__':
    pass
