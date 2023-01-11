import numpy as np
from src.matrix import Matrix
from src.gauss import Gaussian
from src.cross import CrossSection

class Spectr:
    def __init__(self, source: Matrix) -> None:
        self.source = source
        self.is_channelview = True

        self.data = self.__calc()
    
    def to_energy_view(self) -> None:
        pass

    def to_channelview(self) -> None:
        pass
    
    def calc_fwhm(self) -> np.ndarray:
        pass

    def calc_areas(self) -> np.ndarray:
        pass

    def clean_up(self) -> str:
        pass

    def get_baseline(self) -> str:
        pass

    def to_workbook(self) -> str:
        pass

    def __peak_search(self) -> np.ndarray:
        pass

    def __all_ranges(self) -> np.ndarray:
        pass

    def __calc(self) -> np.ndarray:
        result = np.array([np.arange(0, 256, 1, dtype=np.uint32), np.zeros(self.source.dim, dtype=np.uint32)])

        for i in range(result.shape[0]):
            result[1, i] = self.source.components[i, :].sum()

        return result