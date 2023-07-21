import struct
import numpy as np

from business.matrix import Matrix, Spectrum, Locus, NucleiConverter


BEAM_CHARGE = 0
BEAM_NUCLON = 1
TARGET_CHARGE = 2
TARGET_NUCLON = 3
BEAM_ENERGY = 4
DETECTOR_ANGLE = 8

E_DETECTOR_THICKNESS = 12
E_DETECTOR_MADEOF = 16
DE_DETECTOR_THICKNESS = 20
DE_DETECTOR_RHICKNESS = 24

INTEGRATOR_COUNTS = 28
CONGRUENCE = 32
INTEGRATOR_CONSTANT = 36
COLLIMATOR_RADIUS = 40
TARGET_DETECTOR_DISTANCE = 44

E_SIZE = 48
DE_SIZE = 50
MATRIX_START = 52

LOCUSES_START = lambda height, width: 4 * height * width

class Encoder:
    def __init__(self, matrix: Matrix, directory: str) -> None:
        self.matrix = matrix
        self.directory = directory

    def write_down(self) -> None:
        path = self.generate_file_name()
        buffer = open(path, 'wb')

    def generate_file_name(self) -> str:
        beam_name = NucleiConverter.to_string(self.matrix.experiment.beam)
        target_name = NucleiConverter.to_string(self.matrix.experiment.target)
        energy = self.matrix.experiment.beam_energy
        angle = self.matrix.angle

        return f'{target_name}+{beam_name}_{round(energy, 1)}MeV_{angle}.ds'


class Decoder:
    def __init__(self, path: str) -> None:
        self.buffer = open(path, 'rb').read()


if __name__ == '__main__':
    pass
