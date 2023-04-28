import numpy as np

class USBParser:
    def __init__(self, path: str) -> None:
        self.path = path

    def get_matrix(self) -> np.ndarray:
        pass

    def get_angle(self) -> np.ndarray:
        pass

    def get_integrator_parameters(self) -> float:
        pass

    def get_misscalculation(self) -> float:
        pass

if __name__ == '__main__':
    pass
