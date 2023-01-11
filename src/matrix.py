from __future__ import annotations

import numpy as np
from matplotlib import cm

class Matrix:
    RGB = 3
    colormap_types = [
        'plasma',
        'inferno',
        'virdis',
        'magma'
        'cividis'
    ]

    def __init__(self, path: str, colormap: str = 'plasma') -> None:
        self.path = path
        self.colormap = colormap

        self.components = self.__make_matrix()
        self.dim = self.components.shape 

    @property
    def rescale(self) -> np.ndarray:
        transform_const = 255 / (self.components.max() - self.components.min())
        result = self.components - self.components.min()

        return result * transform_const

    def get_colormap_values(self, rate: int) -> list[int]:
        if rate < 0 or rate > 255: return [0, 0, 0]
        if rate == 0: return [255, 255, 255]

        mapper = cm.get_cmap(self.colormap, 256).colors[:, :Matrix.RGB]
        mapper = (mapper * 255).astype(np.uint8) 

        return [mapper[rate, i] for i in range(Matrix.RGB)]

    def cut(self, dots: np.ndarray) -> Matrix:
        pass
    
    def __make_matrix(self) -> np.ndarray:
        return np.loadtxt(self.path, dtype=np.uint8, delimiter=',').reshape(256, 256)