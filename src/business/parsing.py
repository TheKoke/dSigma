import struct
import numpy

from business.yard import NucleiConverter
from business.physics import Nuclei, PhysicalExperiment


# Binary Coordinates (offsets for struct module)
DE_SIZE      = 0
E_SIZE       = 2
TIMER        = 4
FULLTIME     = 8
CONGRUENCE   = 12
MONITOR      = 16
INTEGRATOR   = 20
MATRIX_START = 28
# Coordinates of this ones depends on matrix sizes, that is why they are lambda functions
BEAM_NAME        = lambda length, width: MATRIX_START + length * width * 4 + 20
BEAM_ENERGY      = lambda length, width: MATRIX_START + length * width * 4 + 25
INTEGRATOR_CONST = lambda length, width: MATRIX_START + length * width * 4 + 29
TARGET_NAME      = lambda length, width: MATRIX_START + length * width * 4 + 33
DETECTOR_ANGLE   = lambda length, width: MATRIX_START + length * width * 4 + 82
DE_THICKNESS     = lambda length, width: MATRIX_START + length * width * 4 + 86
LOCUSES_START    = lambda length, width: MATRIX_START + length * width * 4 + 115

INTEGER_BINARY_SIZE = 4 # bytes


class USBParser:
    def __init__(self, path: str) -> None:
        self.buffer = open(path, 'rb').read()

    @property
    def matrix_sizes(self) -> tuple[int, int]:
        de_size = struct.unpack_from('H', self.buffer, DE_SIZE)[0]
        e_size =  struct.unpack_from('H', self.buffer, E_SIZE)[0]
        return (de_size, e_size)
    
    def get_matrix(self) -> numpy.ndarray:
        temp = []
        for i in range(self.matrix_sizes[0] * self.matrix_sizes[1]):
            temp.append(struct.unpack_from('I', self.buffer, MATRIX_START + 4 * i)[0])

        temp = numpy.array(temp)
        return temp.reshape(self.matrix_sizes[0], self.matrix_sizes[1])

    def get_angle(self) -> float:
        coordinate = DETECTOR_ANGLE(*self.matrix_sizes)
        return struct.unpack_from('f', self.buffer, coordinate)[0]

    def get_integrator_counts(self) -> int:
        return struct.unpack_from('i', self.buffer, INTEGRATOR)[0]

    def get_misscalculation(self) -> int:
        matrix_sum = self.get_matrix().sum()
        congruence = struct.unpack_from('i', self.buffer, CONGRUENCE)[0]
        return congruence / matrix_sum

    def get_experiment(self) -> PhysicalExperiment:
        beam = self.parse_beam()
        target = self.parse_target()
        energy = self.parse_beam_energy()

        return PhysicalExperiment(beam, target, energy)
    
    def parse_beam(self) -> Nuclei:
        coordinate = BEAM_NAME(*self.matrix_sizes)
        name = struct.unpack_from('5s', self.buffer, coordinate)[0].decode('ascii')
        return NucleiConverter.to_nuclei(name)

    def parse_target(self) -> Nuclei:
        coordinate = TARGET_NAME(*self.matrix_sizes)
        name = struct.unpack_from('5s', self.buffer, coordinate)[0].decode('ascii')
        return NucleiConverter.to_nuclei(name)
    
    def parse_beam_energy(self) -> float:
        coordinate = BEAM_ENERGY(*self.matrix_sizes)
        return struct.unpack_from('f', self.buffer, coordinate)[0]
    
    def take_locuses(self) -> dict[Nuclei, list[tuple[int, int]]]:
        result = dict()
        queue = [Nuclei(1, 1), Nuclei(1, 2), Nuclei(1, 3), Nuclei(2, 3), Nuclei(2, 4)]
        
        current_locus_start = LOCUSES_START(*self.matrix_sizes)
        for locus in queue:
            current_locus_size = struct.unpack_from('i', self.buffer, current_locus_start)[0]
            current_locus_start += INTEGER_BINARY_SIZE

            result[locus] = self.accumulate_locus(current_locus_size, current_locus_start)
            current_locus_start += 2 * INTEGER_BINARY_SIZE * current_locus_size

        return result
    
    def accumulate_locus(self, count: int, start: int) -> list[tuple[int, int]]:
        locus_positions = []
        for i in range(count):
            locus_positions.append(
                (
                    struct.unpack_from('i', self.buffer, start + 2 * i * INTEGER_BINARY_SIZE)[0], 
                    struct.unpack_from('i', self.buffer, start + (2 * i + 1) * INTEGER_BINARY_SIZE)[0]
                )
            )

        return USBParser.to_cartesian(locus_positions)
    
    @staticmethod
    def to_cartesian(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        WINEDE_WINDOW_ZOOM = 2
        WINEDE_WINDOW_SHIFT = 604

        return [
            (   
                point[0] // WINEDE_WINDOW_ZOOM, 
                (WINEDE_WINDOW_SHIFT - point[1]) // WINEDE_WINDOW_ZOOM
            ) for point in points
        ]


if __name__ == '__main__':
    pass
