import numpy as np

class Gaussian:
    '''
    W(x) = 1/(sqrt(2pi * sigma) * exp{-(x - <x>)^2 / 2sigma})
    sigma = sqrt(1/(N - 1) * Sum(i, N, (x(i) - <x>)^2)
    sigma -> dispersion
    '''
    def __init__(self, x: np.ndarray, y: np.ndarray) -> None:
        self.x = x
        self.y = y

    def peak_center(self) -> np.float64:
        return self.x[self.y.argmax()]

    def area(self) -> np.float64:
        return self.full_width_half_might() / np.sqrt(2 * np.log(2)) \
            * self.max_height() * np.sqrt(np.pi / 2)

    def full_width_half_might(self) -> np.float64:
        return self.dispersion() / (2 * np.sqrt(2 * np.log(2)))

    def up_shift(self) -> np.float64:
        return self.y.min()

    def max_height(self) -> np.float64:
        return self.y.max()

    def probability(self) -> np.ndarray:
        constant = self.area() / (self.full_width_half_might() * np.sqrt(np.pi / (4 * np.log(2))))

        exp_constant = -1 * (4 * np.log(2)) / (self.full_width_half_might() ** 2)
        array_part = (self.x - self.peak_center()) ** 2

        return self.up_shift() + constant * np.exp(exp_constant * array_part)
    
    def arithmetic_mean(self) -> np.float64:
        return self.x.mean()

    def dispersion(self) -> np.float64:
        mean = self.arithmetic_mean()
        return np.sum((self.x - mean) ** 2, dtype=np.float64) / (len(self.x) - 1)