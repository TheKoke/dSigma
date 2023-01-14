from __future__ import annotations

import numpy as np
from parsing import USBParser

class Matrix:
    def __init__(self, path: str, sizes: int) -> None:
        self.path = path
        self.sizes = sizes

        self.components = self.__make_matrix()
        self.dim = self.components.shape 

    def rescale(self) -> np.ndarray:
        transform_const = 255 / (self.components.max() - self.components.min())
        result = self.components - self.components.min()

        return result * transform_const

    def bright_up(self, amount: np.uint8) -> np.ndarray:
        pass

    def bright_down(self, amount: np.uint8) -> np.ndarray:
        pass

    def cut(self, dots: np.ndarray) -> Matrix:
        pass
    
    def __make_matrix(self) -> np.ndarray:
        if self.path.split('.')[1] == 'usb':
            u = USBParser(self.path, self.sizes)
            u.set_binary(48, 4 * self.sizes ** 2 + 48, 4)

            return u.generate_matrix()

        if self.path.split('.')[1] == 'txt':
            return np.loadtxt(self.path, delimiter=',')