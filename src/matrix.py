from __future__ import annotations

import numpy as np
from matplotlib import cm
from spectr import Spectr

class Matrixograph:
    '''
    Class of controller Matrix model.
    '''

    RGB = 3

    def __init__(self, path: str, colormap: str = 'plasma') -> None:
        self.path = path
        self.colormap = colormap

        self.matrix: Matrix = self.__make_matrix()

    def get_colormap_values(self, rate: int) -> list[int]:
        if rate < 0 or rate > 255:
            return [0, 0, 0]

        if rate == 0:
            return [255, 255, 255]

        mapper = cm.get_cmap(self.colormap, 256).colors[:, :Matrixograph.RGB]
        mapper = (mapper * 255).astype(np.uint8) 

        return [mapper[rate, i] for i in range(Matrixograph.RGB)]

        
    def rescale(self) -> np.ndarray:
        transform_const = 255 / (self.matrix.components.max() - self.matrix.components.min())

        result = self.matrix.components - self.matrix.components.min()

        return result * transform_const
    
    def __make_matrix(self) -> Matrix:
        return Matrix(np.loadtxt(self.path, dtype=np.uint8, delimiter=','))

class Matrix:
    def __init__(self, components: np.ndarray) -> None:
        self.components = components
        self.dim = len(components)

    def cut(self, dots: list) -> Matrix:
        pass

    def to_spectr(self) -> Spectr:
        return Spectr(self)