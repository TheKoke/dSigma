import struct
import numpy

from business.yard import NucleiConverter
from business.matrix import Matrix, Locus
from business.analysis import Spectrum, Gaussian
from business.electronics import Telescope, Detector
from business.physics import Nuclei, PhysicalExperiment


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
        struct.pack_into('4s', buffer, E_DETECTOR_MADEOF, e_detector.madeof)

        struct.pack_into('f', buffer, DE_DETECTOR_THICKNESS, de_detector.thickness)
        struct.pack_into('4s', buffer, DE_DETECTOR_MADEOF, de_detector.madeof)

    def write_details(self, buffer: bytearray) -> None:
        integrator_count = self.matrix.integrator
        integrator_constant = 0
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

        return self.directory + f'{target_name}+{beam_name}_{round(energy)}MeV_{angle}.ds'
    
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


class Decoder:
    def __init__(self, path: str) -> None:
        self.buffer = open(path, 'rb').read()

    @property
    def matrix_sizes(self) -> tuple[int, int]:
        e_size = struct.unpack_from('H', self.buffer, E_SIZE)[0]
        de_size = struct.unpack_from('H', self.buffer, DE_SIZE)[0]

        return (e_size, de_size)

    def get_experiment(self) -> PhysicalExperiment:
        beam = self.parse_beam()
        target = self.parse_target()
        energy = self.parse_beam_energy()

        return PhysicalExperiment(beam, target, energy)

    def parse_beam(self) -> Nuclei:
        charge = struct.unpack_from('B', self.buffer, BEAM_CHARGE)[0]
        nuclons = struct.unpack_from('B', self.buffer, BEAM_NUCLON)[0]

        return Nuclei(charge, nuclons)

    def parse_target(self) -> Nuclei:
        charge = struct.unpack_from('B', self.buffer, TARGET_CHARGE)[0]
        nuclons = struct.unpack_from('B', self.buffer, TARGET_NUCLON)[0]

        return Nuclei(charge, nuclons)

    def parse_beam_energy(self) -> float:
        return struct.unpack_from('f', self.buffer, BEAM_ENERGY)[0]

    def get_electronics(self) -> Telescope:
        e_thick = struct.unpack_from('f', self.buffer, E_DETECTOR_THICKNESS)[0]
        e_madeof = struct.unpack_from('4s', self.buffer, E_DETECTOR_MADEOF)[0].decode('ascii')

        de_thick = struct.unpack_from('f', self.buffer, DE_DETECTOR_THICKNESS)[0]
        de_madeof = struct.unpack_from('4s', self.buffer, DE_DETECTOR_MADEOF)[0].decode('ascii')

        collimator = struct.unpack_from('f', self.buffer, COLLIMATOR_RADIUS)[0]
        distance = struct.unpack_from('f', self.buffer, TARGET_DETECTOR_DISTANCE)[0]

        stopping = Detector(e_madeof, e_thick)
        piercing = Detector(de_madeof, de_thick)

        return Telescope(stopping, piercing, collimator, distance)

    def get_angle(self) -> float:
        return struct.unpack_from('f', self.buffer, DETECTOR_ANGLE)[0]

    def get_integrator_counts(self) -> int:
        return struct.unpack_from('I', self.buffer, INTEGRATOR_COUNTS)[0]

    def get_integrator_constant(self) -> float:
        return struct.unpack_from('f', self.buffer, INTEGRATOR_CONSTANT)[0]

    def get_misscalculation(self) -> float:
        congruence = struct.unpack_from('I', self.buffer, CONGRUENCE)[0]
        matrix = self.get_matrix()

        return congruence / matrix.sum()

    def get_matrix(self) -> numpy.ndarray:
        e_size, de_size = self.matrix_sizes
        flat = [struct.unpack_from('I', self.buffer, MATRIX_START + 4 * i)[0] for i in range(e_size * de_size)]
        return numpy.array(flat).reshape(de_size, e_size)

    def take_locuses(self) -> list[Locus]:
        matrix = self.get_matrix()

        offset = LOCUSES_START(*self.matrix_sizes)
        count = struct.unpack_from('H', self.buffer, offset)[0]
        offset += 1

        collected = []
        for _ in range(count):
            z = struct.unpack_from('B', self.buffer, offset)[0]
            offset += 1

            a = struct.unpack_from('B', self.buffer, offset)[0]
            offset += 1

            points_count = struct.unpack_from('I', self.buffer, offset)[0]
            offset += 4

            current_points = []
            for _ in range(points_count):
                e_coordinate = struct.unpack_from('H', self.buffer, offset)[0]
                de_coordinate = struct.unpack_from('H', self.buffer, offset + 2)[0]

                current_points.append((e_coordinate, de_coordinate))
                offset += 4

            collected.append(Locus(Nuclei(a, z), matrix, current_points))

        return collected

    def take_spectrums(self) -> list[Spectrum]:
        locuses_size = sum([6 + 4 * len(locus.points) for locus in self.take_locuses()]) + 2
        offset = LOCUSES_START(*self.matrix_sizes) + locuses_size

        angle = self.get_angle()
        electronics = self.get_electronics()
        experiment = self.get_experiment()

        collected = []
        while offset >= len(self.buffer):
            current_nuclei_charge = struct.unpack_from('B', self.buffer, offset)[0]
            current_nuclei_nuclons = struct.unpack_from('B', self.buffer, offset + 1)[0]
            offset += 2

            current_reaction = experiment.create_reaction(Nuclei(current_nuclei_charge, current_nuclei_nuclons))
            current_spectrum = Spectrum(current_reaction, angle, electronics, [])

            peaks_count = struct.unpack_from('H', self.buffer, offset)[0]
            offset += 2

            for _ in range(peaks_count):
                gathered = self.__gather_peak(offset)
                current_spectrum.add_peak(gathered[0], gathered[1])

            offset += 16
            collected.append(current_spectrum)

        return collected
    
    def __gather_peak(self, offset: int) -> tuple[float, Gaussian]:
        state = struct.unpack_from('f', self.buffer, offset)[0]
        offset += 4

        center = struct.unpack_from('I', self.buffer, offset)[0]
        offset += 4

        fwhm = struct.unpack_from('f', self.buffer, offset)[0]
        offset += 4

        area = struct.unpack_from('f', self.buffer, offset)[0]
        return (state, Gaussian(center, fwhm, area))


if __name__ == '__main__':
    pass
