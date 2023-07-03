import struct
import numpy as np

from business.physics import Nuclei
from business.yard import NucleiConverter


# Binary coordinates
#      (start, size)
E_SIZE = (0, 2)
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
POSSIBLE_LOCUSES = ['p', 'd', 't', 'he3', 'he4']

BITES_PER_BYTE = 8
INTEGER_BINARY_SIZE = 4


def generate_binary_string(number: int) -> str:
    return bin(number)[2:].zfill(BITES_PER_BYTE)

def binary_to_float(binary: str) -> float:
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

def binary_to_int(buffer: bytes, start: int, size: int) -> int:
    result = ''
    for i in range(start, start + size):
        result = generate_binary_string(buffer[i]) + result

    return int(result, 2)

def parsing_float(buffer: bytes, binary_start: int, binary_size: int) -> float:
    integer_value = binary_to_int(buffer, binary_start, binary_size)
    return binary_to_float(bin(integer_value))


class USBParser:
    def __init__(self, path: str) -> None:
        self.path = path
        self.sizes = self.find_out_sizes()

    def find_out_sizes(self) -> tuple[int, int]:
        buffer = open(self.path, 'rb').read()
        e_channels = binary_to_int(buffer, E_SIZE[0], E_SIZE[1])
        de_channels =  binary_to_int(buffer, DE_SIZE[0], DE_SIZE[1])

        return (e_channels, de_channels)
    
    def get_matrix(self) -> np.ndarray:
        buffer = open(self.path, 'rb').read()
        temp = []
        for i in range(MATRIX_START, MATRIX_START + self.sizes[0] * self.sizes[1], INTEGER_BINARY_SIZE):
            temp.append(int(buffer[i]))

        temp = np.array(temp)
        return temp.reshape(self.sizes[1], self.sizes[0])
    
    def get_angle(self) -> float:
        coordinates = DETECTOR_ANGLE(self.sizes[0], self.sizes[1])
        return parsing_float(open(self.path, 'rb'), coordinates[0], coordinates[1])

    def get_integrator_counts(self) -> int:
        buffer = open(self.path, 'rb').read()
        return binary_to_int(buffer, INTEGRATOR[0], INTEGRATOR[1])

    def get_misscalculation(self) -> int:
        buffer = open(self.path, 'rb').read()
        return binary_to_int(buffer, CONGRUENCE[0], CONGRUENCE[1])
    
    def parse_beam(self) -> Nuclei:
        return self.__parsing_nucleis(BEAM_NAME)

    def parse_target(self) -> Nuclei:
        return self.__parsing_nucleis(TARGET_NAME)
    
    def get_beam_energy(self) -> float:
        coordinates = BEAM_ENERGY(self.sizes[0], self.sizes[1])
        return parsing_float(open(self.path, 'rb'), coordinates[0], coordinates[1])
    
    def __parsing_nucleis(self, position) -> Nuclei:
        buffer = open(self.path, 'rb').read()
        binary_coordinates = position(self.sizes[0], self.sizes[1])

        name = self.__parsing_str(buffer, binary_coordinates[0], binary_coordinates[1])
        return NucleiConverter.to_nuclei(name)
    
    def __parsing_str(self, buffer: bytes, binary_start: int, binary_size: int) -> str:
        collected = ''
        for i in range(binary_start, binary_start + binary_size):
            collected += chr(buffer[i])

        return collected.replace(' ', '')

    def take_locuses(self) -> dict[str, list[tuple[int, int]]]:
        result = dict()
        buffer = open(self.path, 'rb').read()

        current_locus_start = LOCUSES_START(self.sizes[0], self.sizes[1])
        for locus in POSSIBLE_LOCUSES:
            current_size = binary_to_int(buffer, current_locus_start, INTEGER_BINARY_SIZE)
            current_locus_start += INTEGER_BINARY_SIZE

            result[locus] = self.accumulate_locus(current_size, current_locus_start)
            
            current_locus_start += 2 * INTEGER_BINARY_SIZE * current_size

        return result
    
    def accumulate_locus(self, size: int, start: int) -> list[tuple[int, int]]:
        buffer = open(self.path, 'rb').read()

        locus_positions = []
        for i in range(size):
            locus_positions.append((
                binary_to_int(buffer, start + 8 * i, INTEGER_BINARY_SIZE), 
                binary_to_int(buffer, start + 8 * i + INTEGER_BINARY_SIZE, INTEGER_BINARY_SIZE)
            ))

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
