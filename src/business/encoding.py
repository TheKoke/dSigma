import struct
import numpy

from business.matrix import (
    Matrix, Spectrum, Locus,
    NucleiConverter, Telescope, 
    Nuclei, PhysicalExperiment
)

# Physics area
BEAM_CHARGE = 0
BEAM_NUCLON = 1
TARGET_CHARGE = 2
TARGET_NUCLON = 3
BEAM_ENERGY = 4
DETECTOR_ANGLE = 8
# Electronics area
E_DETECTOR_THICKNESS = 12
E_DETECTOR_MADEOF = 16
DE_DETECTOR_THICKNESS = 20
DE_DETECTOR_MADEOF = 24
# Cross-section valuable, details area
INTEGRATOR_COUNTS = 28
CONGRUENCE = 32
INTEGRATOR_CONSTANT = 36
COLLIMATOR_RADIUS = 40
TARGET_DETECTOR_DISTANCE = 44
# Matrix area
E_SIZE = 48
DE_SIZE = 50
MATRIX_START = 52
# Dynamic area, locuses and spectres
LOCUSES_START = lambda height, width: 4 * height * width


class Encoder:
    def __init__(self, matrix: Matrix, directory: str) -> None:
        self.matrix = matrix
        self.directory = directory

    def write_down(self) -> str:
        path = self.generate_file_name()
        buffer = bytearray(self.calc_byte_size())

        self.write_physics(buffer)
        self.write_electronics(buffer)
        self.write_details(buffer)
        self.write_matrix(buffer)
        self.write_locuses(buffer)
        self.write_spectrums(buffer)

        binary = open(path, 'wb')
        binary.write(buffer)
        binary.close()

        return path

    def write_physics(self, buffer: bytearray) -> None:
        pass

    def write_electronics(self, buffer: bytearray) -> None:
        pass

    def write_details(self, buffer: bytearray) -> None:
        pass

    def write_matrix(self, buffer: bytearray) -> None:
        pass

    def write_locuses(self, buffer: bytearray) -> int:
        pass

    def write_spectrums(self, buffer: bytearray) -> int:
        pass

    def generate_file_name(self) -> str:
        beam_name = NucleiConverter.to_string(self.matrix.experiment.beam)
        target_name = NucleiConverter.to_string(self.matrix.experiment.target)
        energy = self.matrix.experiment.beam_energy
        angle = self.matrix.angle

        return self.directory + f'{target_name}+{beam_name}_{round(energy, 1)}MeV_{angle}.ds'
    
    def calc_byte_size(self) -> int:
        physical_area_size = 12
        electronics_area_size = 16
        details_area_size = 20
        matrix_area_size = 4 + 4 * len(self.matrix.numbers.flat)

        locuses_area_size = 0
        for locus in self.matrix.locuses:
            locuses_area_size += 4 + 4 * len(locus.points)

        spectrums_area_size = 0
        for spectrum in self.matrix.spectrums:
            spectrums_area_size += 4 + 12 * len(spectrum.theory_peaks) # CROUTCH. FIX THE ANALYSIS MODULE

        return physical_area_size + electronics_area_size + \
            details_area_size + matrix_area_size + \
            locuses_area_size + spectrums_area_size


class Decoder:
    def __init__(self, path: str) -> None:
        self.buffer = open(path, 'rb').read()

    @property
    def matrix_sizes(self) -> tuple[int, int]:
        pass

    def gather_matrix(self) -> Matrix:
        pass

    def get_experiment(self) -> PhysicalExperiment:
        pass

    def parse_beam(self) -> Nuclei:
        pass

    def parse_target(self) -> Nuclei:
        pass

    def parse_beam_energy(self) -> float:
        pass

    def get_electronics(self) -> Telescope:
        pass

    def get_angle(self) -> float:
        pass

    def get_integrator_counts(self) -> int:
        pass

    def get_integrator_constant(self) -> float:
        pass

    def get_misscalculation(self) -> float:
        pass

    def get_matrix(self) -> numpy.ndarray:
        pass

    def take_locuses(self) -> list[Locus]:
        pass

    def take_spectrums(self) -> list[Spectrum]:
        pass


if __name__ == '__main__':
    pass
