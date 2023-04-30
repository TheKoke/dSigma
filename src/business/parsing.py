import numpy as np

# Binary coordinates
E_SIZE = 0
DE_SIZE = 2
TIMER = 4
FULLTIME = 8
CONGRUENCE = 12
MONITOR = 16
INTEGRATOR = 20
MATRIX_START = 28

BEAM_NAME = lambda length, width: length * width * 4 + 20
BEAM_ENERGY = lambda length, width: length * width * 4 + 25
INTEGRATOR_CONST = lambda length, width: length * width * 4 + 29
TARGET_NAME = lambda length, width: length * width * 4 + 33
DETECTOR_ANGLE = lambda length, width: length * width * 4 + 82
DE_THICKNESS = lambda length, width: length * width * 4 + 86
LOCUSES_START = lambda length, width: length * width * 4 + 114


class USBParser:
    def __init__(self, path: str) -> None:
        self.path = path

    def generate_lab_report(self) -> str:
        pass

    def find_out_sizes(self) -> tuple[int, int]:
        buffer = open(self.path, 'rb').read()
        return (int(buffer[E_SIZE]), int(buffer[DE_SIZE]))
    
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
        return DETECTOR_ANGLE(sizes[0], sizes[1])

    def get_integrator_counts(self) -> int:
        buffer = open(self.path, 'rb').read()
        return int(buffer[INTEGRATOR])

    def get_misscalculation(self) -> float:
        buffer = open(self.path, 'rb').read()
        return int(buffer[CONGRUENCE])

    def target_properties(self) -> dict[str, float]:
        pass

    def take_locuses(self) -> dict[str, list[tuple[int, int]]]:
        pass


class ReactionParser:
    def __init__(self, path: str) -> None:
        self.path = path



if __name__ == '__main__':
    pass
