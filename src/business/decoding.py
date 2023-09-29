import struct
import numpy

from business.locus import Locus
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
E_DETECTOR_RESOLUTION = 20
DE_DETECTOR_THICKNESS = 24
DE_DETECTOR_MADEOF    = 28
DE_DETECTOR_RESOLUTION = 32
# Cross-section valuable, details area
INTEGRATOR_COUNTS        = 36
CONGRUENCE               = 40
INTEGRATOR_CONSTANT      = 44
COLLIMATOR_RADIUS        = 48
TARGET_DETECTOR_DISTANCE = 52
# Matrix area
E_SIZE       = 56
DE_SIZE      = 58
MATRIX_START = 60
# Dynamic area, locuses and spectres
LOCUSES_START = lambda height, width: MATRIX_START + 4 * height * width


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
        e_res = struct.unpack_from('f', self.buffer, E_DETECTOR_RESOLUTION)[0]

        de_thick = struct.unpack_from('f', self.buffer, DE_DETECTOR_THICKNESS)[0]
        de_madeof = struct.unpack_from('4s', self.buffer, DE_DETECTOR_MADEOF)[0].decode('ascii')
        de_res = struct.unpack_from('f', self.buffer, DE_DETECTOR_RESOLUTION)[0]

        collimator = struct.unpack_from('f', self.buffer, COLLIMATOR_RADIUS)[0]
        distance = struct.unpack_from('f', self.buffer, TARGET_DETECTOR_DISTANCE)[0]

        stopping = Detector(e_madeof, e_thick, e_res * 1e-3)
        piercing = Detector(de_madeof, de_thick, de_res * 1e-3)

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
        offset += 2

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

            collected.append(Locus(Nuclei(z, a), matrix, current_points))

        return collected

    def take_spectrums(self) -> dict[Nuclei, Spectrum]:
        locuses_size = sum([6 + 4 * len(locus.points) for locus in self.take_locuses()]) + 2
        offset = LOCUSES_START(*self.matrix_sizes) + locuses_size

        angle = self.get_angle()
        electronics = self.get_electronics()
        experiment = self.get_experiment()
        locuses = self.take_locuses()

        collected = dict()
        while offset < len(self.buffer):
            current_nuclei_charge = struct.unpack_from('B', self.buffer, offset)[0]
            current_nuclei_nuclons = struct.unpack_from('B', self.buffer, offset + 1)[0]
            current_nuclei = Nuclei(current_nuclei_charge, current_nuclei_nuclons)
            offset += 2

            current_reaction = experiment.create_reaction(current_nuclei)
            current_locus = next(i for i in locuses if i.particle == current_nuclei)

            current_spectrum = Spectrum(current_reaction, angle, electronics, current_locus.to_spectrum())

            calib_e0 = struct.unpack_from('f', self.buffer, offset)[0]
            calib_k = struct.unpack_from('f', self.buffer, offset + 4)[0]
            offset += 8

            current_spectrum.scale_shift = calib_e0
            current_spectrum.scale_value = calib_k

            peaks_count = struct.unpack_from('H', self.buffer, offset)[0]
            offset += 2

            for _ in range(peaks_count):
                gathered = self.__gather_peak(offset)
                current_spectrum.add_peak(gathered[0], gathered[1])
                offset += 16
            
            collected[current_nuclei] = current_spectrum

        return collected
    
    def __gather_peak(self, offset: int) -> tuple[float, Gaussian]:
        state = struct.unpack_from('f', self.buffer, offset)[0]
        offset += 4

        center = struct.unpack_from('f', self.buffer, offset)[0]
        offset += 4

        dispersion = struct.unpack_from('f', self.buffer, offset)[0]
        offset += 4

        area = struct.unpack_from('f', self.buffer, offset)[0]
        return (round(state, 3), Gaussian(center, dispersion, area))
    

if __name__ == '__main__':
    pass
