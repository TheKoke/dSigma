from __future__ import annotations

import numpy
from matplotlib import cm
import matplotlib.pyplot as plt

class Matrixograph:
    def __init__(self, path: str, colormap: str = 'plasma') -> None:
        self.path = self
        self.colormap_name = colormap

        self.matrix: Matrix = Matrix()

class Matrix:
    pass