import numpy as np
from src.matrix import Matrix

class Spectrograph:
    pass

class Spectr:
    def __init__(self, source: Matrix) -> None:
        self.source = source

        self.components = self.__calc()
    
    def clean_up(self) -> str:
        pass

    def get_baseline(self) -> str:
        pass

    def __calc(self) -> np.ndarray:
        result = np.array([np.arange(0, 256, 1, dtype=np.uint32), np.zeros(self.source.dim, dtype=np.uint32)])

        for i in range(len(result)):
            result[1, i] = self.source.components[i, :].sum()

        return result