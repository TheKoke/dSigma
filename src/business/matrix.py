from __future__ import annotations

import numpy as np
from parsing import USBParser

class Matrix:
    def __init__(self, parser: USBParser) -> None:
        self.angle = parser.get_angle()
        self.integrator_count = parser.get_integrator_parameters()
        self.misscalculation = parser.get_misscalc()

        self.numbers = parser.get_matrix()

    def rescale(self) -> np.ndarray:
        transform_const = 255 / (self.numbers.max() - self.numbers.min())
        result = self.numbers - self.numbers.min()

        return result * transform_const

    def bright_up(self, amount: int) -> np.ndarray:
        pass

    def bright_down(self, amount: int) -> np.ndarray:
        pass

    def cut(self, dots: np.ndarray) -> Matrix:
        pass


if __name__ == '__main__':
    pass