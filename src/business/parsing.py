import struct
import numpy as np
from physics import Nuclei, Reaction

# Binary coordinates
E_SIZE = (0, 2) # (start, size)
DE_SIZE = (2, 2)
TIMER = (4, 4)
FULLTIME = (8, 4)
CONGRUENCE = (12, 4)
MONITOR = (16, 4)
INTEGRATOR = (20, 4)
MATRIX_START = 28

BEAM_NAME = lambda length, width: (MATRIX_START + length * width * 4 + 20, 5)
BEAM_ENERGY = lambda length, width: (MATRIX_START + length * width * 4 + 25, 4)
INTEGRATOR_CONST = lambda length, width: (MATRIX_START + length * width * 4 + 29, 4)
TARGET_NAME = lambda length, width: (MATRIX_START + length * width * 4 + 33, 5)
DETECTOR_ANGLE = lambda length, width: (MATRIX_START + length * width * 4 + 82, 4)
DE_THICKNESS = lambda length, width: (MATRIX_START + length * width * 4 + 86, 4)
LOCUSES_START = lambda length, width: MATRIX_START + length * width * 4 + 115
POSSIBLE_LOCUSES = ['p', 'd', 't', 'he-3', 'he-4']

BITES_PER_BYTE = 8
INTEGER_BINARY_SIZE = 4


def generate_binary_string(number: int) -> str:
    return bin(number)[2:].zfill(BITES_PER_BYTE)

def binary_to_float(binary: str) -> float:
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def binary_sum(buffer: bytes, start: int, size: int) -> int:
        result = ''
        for i in range(start, start + size):
            result = generate_binary_string(buffer[i]) + result

        return int(result, 2)


class ReactionParser:
    def __init__(self, path: str) -> None:
        self.path = path

    def all_reactions(self) -> list[Reaction]:
        pass

    def take_reaction(self, locus: str) -> Reaction:
        pass

    def parse_beam(self) -> Nuclei:
        name = ''
        buffer = open(self.path, 'rb').read()

        for i in range(BEAM_NAME()[1]):
            pass

    def parse_target(self) -> Nuclei:
        name = ''
        buffer = open(self.path, 'rb').read()

        for i in range(TARGET_NAME()[1]):
            pass


class USBParser:
    def __init__(self, path: str) -> None:
        self.path = path
        self.reactor = ReactionParser(path)

        self.sizes = self.find_out_sizes()

    def find_out_sizes(self) -> tuple[int, int]:
        buffer = open(self.path, 'rb').read()
        e_channels = binary_sum(buffer, E_SIZE[0], E_SIZE[1])
        de_channels =  binary_sum(buffer, DE_SIZE[0], DE_SIZE[1])

        return (e_channels, de_channels)
    
    def get_matrix(self) -> np.ndarray:
        buffer = open(self.path, 'rb').read()
        temp = []
        for i in range(MATRIX_START, MATRIX_START + self.sizes[0] * self.sizes[1], INTEGER_BINARY_SIZE):
            temp.append(int(buffer[i]))

        temp = np.array(temp)
        return temp.reshape(self.sizes[1], self.sizes[0])

    def get_angle(self) -> float:
        buffer = open(self.path, 'rb').read()

        coordinates = DETECTOR_ANGLE(self.sizes[0], self.sizes[1])
        integer_value = binary_sum(buffer, coordinates[0], coordinates[1])

        return binary_to_float(bin(integer_value))

    def get_integrator_counts(self) -> int:
        buffer = open(self.path, 'rb').read()
        return binary_sum(buffer, INTEGRATOR[0], INTEGRATOR[1])

    def get_misscalculation(self) -> int:
        buffer = open(self.path, 'rb').read()
        return binary_sum(buffer, CONGRUENCE[0], CONGRUENCE[1])

    def take_locuses(self) -> dict[str, list[tuple[int, int]]]:
        result = dict()
        buffer = open(self.path, 'rb').read()

        current_locus_start = LOCUSES_START(self.sizes[0], self.sizes[1])
        for locus in POSSIBLE_LOCUSES:
            current_size = binary_sum(buffer, current_locus_start, INTEGER_BINARY_SIZE)
            current_locus_start += INTEGER_BINARY_SIZE

            result[locus] = self.accumulate_locus(current_size, current_locus_start)
            
            current_locus_start += 2 * INTEGER_BINARY_SIZE * current_size

        return result
    
    def accumulate_locus(self, size: int, start: int) -> list[tuple[int, int]]:
        buffer = open(self.path, 'rb').read()

        locus_positions = []
        for i in range(size - 1):
            locus_positions.append((
                binary_sum(buffer, start + 8 * i, INTEGER_BINARY_SIZE), 
                binary_sum(buffer, start + 8 * i + INTEGER_BINARY_SIZE, INTEGER_BINARY_SIZE)
            ))

        return locus_positions


if __name__ == '__main__':
    usb = USBParser("D:\\Данные по Win EDE\\Win EdE to Python\\Li7+d14_2017_BT_54_b_4.usb")
    print(usb.take_locuses())
