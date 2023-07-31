import struct

from business.electronics import Telescope
from business.yard import NucleiConverter
from business.matrix import Matrix, Demo


# Physics area
BEAM_CHARGE    = 0
BEAM_NUCLON    = 1
TARGET_CHARGE  = 2
TARGET_NUCLON  = 3
BEAM_ENERGY    = 4
DETECTOR_ANGLE = 8
# Electronics area
E_DETECTOR_THICKNESS  = 12
E_DETECTOR_MADEOF     = 16
DE_DETECTOR_THICKNESS = 20
DE_DETECTOR_MADEOF    = 24
# Cross-section valuable, details area
INTEGRATOR_COUNTS        = 28
CONGRUENCE               = 32
INTEGRATOR_CONSTANT      = 36
COLLIMATOR_RADIUS        = 40
TARGET_DETECTOR_DISTANCE = 44
# Matrix area
E_SIZE       = 48
DE_SIZE      = 50
MATRIX_START = 52
# Dynamic area, locuses and spectres
LOCUSES_START = lambda height, width: MATRIX_START + 4 * height * width


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
        beam = self.matrix.experiment.beam
        target = self.matrix.experiment.target
        energy = self.matrix.experiment.beam_energy
        angle = self.matrix.angle

        struct.pack_into('B', buffer, BEAM_CHARGE, beam.charge)
        struct.pack_into('B', buffer, BEAM_NUCLON, beam.nuclons)

        struct.pack_into('B', buffer, TARGET_CHARGE, target.charge)
        struct.pack_into('B', buffer, TARGET_NUCLON, target.nuclons)

        struct.pack_into('f', buffer, BEAM_ENERGY, energy)
        struct.pack_into('f', buffer, DETECTOR_ANGLE, angle)

    def write_electronics(self, buffer: bytearray) -> None:
        telescope = self.matrix.electronics
        e_detector = telescope.e_detector
        de_detector = telescope.de_detector

        struct.pack_into('f', buffer, E_DETECTOR_THICKNESS, e_detector.thickness)
        struct.pack_into('4s', buffer, E_DETECTOR_MADEOF, e_detector.madeof.encode('ascii'))

        struct.pack_into('f', buffer, DE_DETECTOR_THICKNESS, de_detector.thickness)
        struct.pack_into('4s', buffer, DE_DETECTOR_MADEOF, de_detector.madeof.encode('ascii'))

    def write_details(self, buffer: bytearray) -> None:
        integrator_count = self.matrix.integrator_counts
        integrator_constant = self.matrix.integrator_constant
        congruence = int(self.matrix.misscalculation * self.matrix.numbers.sum())
        radius = self.matrix.electronics.collimator_radius
        distance = self.matrix.electronics.distance

        struct.pack_into('I', buffer, INTEGRATOR_COUNTS, integrator_count)
        struct.pack_into('I', buffer, CONGRUENCE, congruence)
        struct.pack_into('f', buffer, INTEGRATOR_CONSTANT, integrator_constant)

        struct.pack_into('f', buffer, COLLIMATOR_RADIUS, radius)
        struct.pack_into('f', buffer, TARGET_DETECTOR_DISTANCE, distance)

    def write_matrix(self, buffer: bytearray) -> None:
        matrix = self.matrix.numbers
        de_length, e_length = self.matrix.numbers.shape

        struct.pack_into('H', buffer, E_SIZE, e_length)
        struct.pack_into('H', buffer, DE_SIZE, de_length)

        for i in range(de_length):
            for j in range(e_length):
                offset = 4 * (i * de_length + j)
                struct.pack_into('I', buffer, MATRIX_START + offset, matrix[i, j])

    def write_locuses(self, buffer: bytearray) -> None:
        offset = LOCUSES_START(*self.matrix.numbers.shape)
        locuses = self.matrix.locuses

        struct.pack_into('H', buffer, offset, len(locuses))
        offset += 2

        for locus in locuses:
            struct.pack_into('B', buffer, offset, locus.particle.charge)
            offset += 1

            struct.pack_into('B', buffer, offset, locus.particle.nuclons)
            offset += 1

            struct.pack_into('I', buffer, offset, len(locus.points))
            offset += 4

            for point in locus.points:
                struct.pack_into('H', buffer, offset, point[0])
                struct.pack_into('H', buffer, offset + 2, point[1])
                offset += 4

    def write_spectrums(self, buffer: bytearray) -> None:
        spectrums_area_size = sum([4 + 16 * len(spectrum.peaks) for spectrum in self.matrix.spectrums])
        offset = self.calc_byte_size() - spectrums_area_size - 1

        for spectrum in self.matrix.spectrums:
            fragment = spectrum.reaction.fragment
            struct.pack_into('B', buffer, offset, fragment.charge)
            offset += 1

            struct.pack_into('B', buffer, offset, fragment.nuclons)
            offset += 1

            peaks_count = len(spectrum.peaks)
            struct.pack_into('H', buffer, offset, peaks_count)
            offset += 2

            for state in spectrum.peaks:
                struct.pack_into('f', buffer, offset, state)
                offset += 4

                struct.pack_into('I', buffer, offset, spectrum.peaks[state].mu)
                offset += 4

                struct.pack_into('f', buffer, offset, spectrum.peaks[state].fwhm)
                offset += 4

                struct.pack_into('f', buffer, offset, spectrum.peaks[state].area)
                offset += 4

    def generate_file_name(self) -> str:
        beam_name = NucleiConverter.to_string(self.matrix.experiment.beam)
        target_name = NucleiConverter.to_string(self.matrix.experiment.target)
        energy = self.matrix.experiment.beam_energy
        angle = self.matrix.angle

        return self.directory + f'/{target_name}+{beam_name}_{round(energy)}MeV_{round(angle)}.ds'
    
    def calc_byte_size(self) -> int:
        physical_area_size = 12
        electronics_area_size = 16
        details_area_size = 20
        matrix_area_size = 4 + 4 * len(self.matrix.numbers.flat)

        locuses_area_size = sum([6 + 4 * len(locus.points) for locus in self.matrix.locuses]) + 2
        spectrums_area_size = sum([4 + 16 * len(spectrum.peaks) for spectrum in self.matrix.spectrums])

        return physical_area_size + electronics_area_size + \
                details_area_size + matrix_area_size + \
                locuses_area_size + spectrums_area_size


class DemoEncoder:
    def __init__(self, demo_matrix: Demo, electronics: Telescope, directory: str) -> None:
        self.demo = demo_matrix
        self.telescope = electronics
        self.directory = directory

    def write_down(self) -> str:
        path = self.generate_file_name()
        buffer = bytearray(self.calc_byte_size())

        self.write_physics(buffer)
        self.write_electronics(buffer)
        self.write_details(buffer)
        self.write_matrix(buffer)
        self.write_locuses(buffer)

        binary = open(path, 'wb')
        binary.write(buffer)
        binary.close()

        return path

    def write_physics(self, buffer: bytearray) -> None:
        beam = self.demo.parser.parse_beam()
        target = self.demo.parser.parse_target()
        energy = self.demo.parser.parse_beam_energy()
        angle = self.demo.angle

        struct.pack_into('B', buffer, BEAM_CHARGE, beam.charge)
        struct.pack_into('B', buffer, BEAM_NUCLON, beam.nuclons)

        struct.pack_into('B', buffer, TARGET_CHARGE, target.charge)
        struct.pack_into('B', buffer, TARGET_NUCLON, target.nuclons)

        struct.pack_into('f', buffer, BEAM_ENERGY, energy)
        struct.pack_into('f', buffer, DETECTOR_ANGLE, angle)

    def write_electronics(self, buffer: bytearray) -> None:
        e_detector = self.telescope.e_detector
        de_detector = self.telescope.de_detector

        struct.pack_into('f', buffer, E_DETECTOR_THICKNESS, e_detector.thickness)
        struct.pack_into('4s', buffer, E_DETECTOR_MADEOF, e_detector.madeof.encode('ascii'))

        struct.pack_into('f', buffer, DE_DETECTOR_THICKNESS, de_detector.thickness)
        struct.pack_into('4s', buffer, DE_DETECTOR_MADEOF, de_detector.madeof.encode('ascii'))

    def write_details(self, buffer: bytearray) -> None:
        integrator_count = self.demo.integrator_counts
        integrator_constant = self.demo.integrator_constant
        congruence = int(self.demo.misscalculation * self.demo.numbers.sum())
        radius = self.telescope.collimator_radius
        distance = self.telescope.distance

        struct.pack_into('I', buffer, INTEGRATOR_COUNTS, integrator_count)
        struct.pack_into('I', buffer, CONGRUENCE, congruence)
        struct.pack_into('f', buffer, INTEGRATOR_CONSTANT, integrator_constant)

        struct.pack_into('f', buffer, COLLIMATOR_RADIUS, radius)
        struct.pack_into('f', buffer, TARGET_DETECTOR_DISTANCE, distance)

    def write_matrix(self, buffer: bytearray) -> None:
        matrix = self.demo.numbers
        de_length, e_length = self.demo.numbers.shape

        struct.pack_into('H', buffer, E_SIZE, e_length)
        struct.pack_into('H', buffer, DE_SIZE, de_length)

        for i in range(de_length):
            for j in range(e_length):
                offset = 4 * (i * de_length + j)
                struct.pack_into('I', buffer, MATRIX_START + offset, matrix[i, j])

    def write_locuses(self, buffer: bytearray) -> None:
        offset = LOCUSES_START(*self.demo.numbers.shape)
        locuses = self.demo.locuses()

        struct.pack_into('H', buffer, offset, len(locuses))
        offset += 2

        for locus in locuses:
            struct.pack_into('B', buffer, offset, locus.particle.charge)
            offset += 1

            struct.pack_into('B', buffer, offset, locus.particle.nuclons)
            offset += 1

            struct.pack_into('I', buffer, offset, len(locus.points))
            offset += 4

            for point in locus.points:
                struct.pack_into('H', buffer, offset, point[0])
                struct.pack_into('H', buffer, offset + 2, point[1])
                offset += 4

    def generate_file_name(self) -> str:
        beam_name = NucleiConverter.to_string(self.demo.parser.parse_beam())
        target_name = NucleiConverter.to_string(self.demo.parser.parse_target())
        energy = self.demo.parser.parse_beam_energy()
        angle = self.demo.angle

        return self.directory + f'/{target_name}+{beam_name}_{round(energy)}MeV_{round(angle)}.ds'
    
    def calc_byte_size(self) -> int:
        physical_area_size = 12
        electronics_area_size = 16
        details_area_size = 20
        matrix_area_size = 4 + 4 * len(self.demo.numbers.flat)

        locuses_area_size = sum([6 + 4 * len(locus.points) for locus in self.demo.locuses()]) + 2

        return physical_area_size + electronics_area_size + \
                details_area_size + matrix_area_size + \
                locuses_area_size


if __name__ == '__main__':
    pass
