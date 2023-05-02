import struct
import numpy as np
from physics import Nuclei, Reaction

# Binary coordinates
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
LOCUSES_START = lambda length, width: length * width * 4 + 114

BITES_PER_BYTE = 8


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


class USBParser:
    def __init__(self, path: str) -> None:
        self.path = path
        self.reactor = ReactionParser(path)

    def generate_lab_report(self) -> str:
        pass

    def find_out_sizes(self) -> tuple[int, int]:
        buffer = open(self.path, 'rb').read()
        e_channels = binary_sum(buffer, E_SIZE[0], E_SIZE[1])
        de_channels =  binary_sum(buffer, DE_SIZE[0], DE_SIZE[1])

        return (e_channels, de_channels)
    
    def def_matrix_end(self) -> int:
        sizes = self.find_out_sizes()
        return MATRIX_START + sizes[0] * sizes[1] * 4

    def get_matrix(self) -> np.ndarray:
        sizes = self.find_out_sizes()

        buffer = open(self.path, 'rb').read()
        temp = []
        for i in range(MATRIX_START, MATRIX_START + sizes[0] * sizes[1], 4):
            temp.append(int(buffer[i]))

        temp = np.array(temp)

        return temp.reshape(sizes[1], sizes[0])

    def get_angle(self) -> float:
        sizes = self.find_out_sizes()
        buffer = open(self.path, 'rb').read()

        coordinates = DETECTOR_ANGLE(sizes[0], sizes[1])
        integer_value = binary_sum(buffer, coordinates[0], coordinates[1])

        return binary_to_float(bin(integer_value))

    def get_integrator_counts(self) -> int:
        buffer = open(self.path, 'rb').read()
        return int(buffer[INTEGRATOR])

    def get_misscalculation(self) -> int:
        buffer = open(self.path, 'rb').read()
        return int(buffer[CONGRUENCE])
    
    def take_all_reactions(self) -> list[Reaction]:
        pass

    def target_properties(self) -> dict[str, float]:
        pass

    def take_locuses(self) -> dict[str, list[tuple[int, int]]]:
        pass


if __name__ == '__main__':
    usb = USBParser("E:\\Данные по Win EDE\\Win EdE to Python\\9Be d_14MeV_38BT_A1.usb")
    print(usb.get_angle())
