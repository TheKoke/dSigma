import numpy as np
from business.physics import Reaction


class Gaussian:
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        self.mu = mu
        self.fwhm = fwhm
        self.area = area

    def to_workbook(self) -> str:
        return f'Peak on mu=({self.mu}) with fwhm=({self.fwhm}) and area under peak=({self.area})'

    def __str__(self) -> str:
        func = 'G(x) = '
        func += f'{np.round(self.area, 3)} / (sqrt(2pi * {np.round(self.dispersion(), 3)}) * '
        func += f'exp(-(x - {np.round(self.mu, 3)})^2 / 2{np.round(self.dispersion(), 3)})'

        return func

    def dispersion(self) -> np.float64:
        return self.fwhm / (2 * np.sqrt(2 * np.log(2)))

    def three_sigma(self) -> np.ndarray:
        sigma = self.dispersion()
        return np.linspace(-3 * sigma + self.mu, 3 * sigma + self.mu, 50)

    def function(self) -> np.ndarray:
        constant = self.area / (self.fwhm * np.sqrt(np.pi / (4 * np.log(2))))
        exp_constant = -1 * (4 * np.log(2)) / (self.fwhm ** 2)

        array_part = (self.three_sigma() - self.mu) ** 2
        return constant * np.exp(exp_constant * array_part)
    

class Lorentzian:
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        self.mu = mu
        self.fwhm = fwhm
        self.area = area

    def to_workbook(self) -> str:
        return f'Peak on mu=({self.mu}) with fwhm=({self.fwhm}) and area under peak=({self.area})'

    def __str__(self) -> str:
        func = 'L(x) = '
        func += f'2 * {round(self.area, 3)} / pi'
        func += f'* [{np.round(self.fwhm, 3)} / ((x - {round(self.mu)})^2 + {round(self.fwhm, 3)}^2)]'

        return func
    
    def dispersion(self) -> float:
        return self.fwhm / (2 * np.sqrt(2 * np.log(2)))
    
    def three_sigma(self) -> np.ndarray:
        sigma = self.dispersion()
        return np.linspace(-5 * sigma + self.mu, 5 * sigma + self.mu, 50)
    
    def function(self) -> np.ndarray:
        constant = 2 * self.area / np.pi
        brackets = self.fwhm / (4 * (self.three_sigma() - self.mu) ** 2 + self.fwhm ** 2)

        return constant * brackets


class CrossSection:
    def __init__(self, reaction: Reaction) -> None:
        '''
        Diff. cross section for reaction A(a, b)B
        '''
        self.A = reaction.target.nuclons; self.a = reaction.beam.nuclons
        self.B = reaction.residual.nuclons; self.b = reaction.fragment.nuclons

        self.integrator_const = 1e-6
        self.norm = 1

        self.distance = 200
        self.collimator_radius = 1.6

        self.reaction_q = reaction.reaction_quit()
        self.beam_energy = reaction.beam_energy

    def set_geometrical_parameters(self, distance: float, collimator_radius: float) -> None:
        self.distance = distance
        self.collimator_radius = collimator_radius

    def set_electronics(self, integrator_const: float, norm: float) -> None:
        self.integrator_const = integrator_const
        self.norm = norm
    
    def formula(self, events: np.ndarray, angles: np.ndarray, integrator: np.ndarray, misscalculation: np.ndarray) -> np.ndarray:
        numerator = self.A * events * misscalculation * self.norm
        denumerator = integrator * self.integrator_const * self.solid_angle()

        return self.g_constant(angles) * numerator / denumerator

    def angle_to_cm(self, angles: np.ndarray) -> np.ndarray:
        x2 = np.sqrt(self.x_square())
        angles_in_rad = angles * np.pi / 180

        multiplier = (x2 * np.sin(angles_in_rad)) ** 2

        return np.arctan(np.sqrt(multiplier) / np.sqrt(1 - multiplier)) * 180 / np.pi + angles

    def solid_angle(self) -> float:
        return 2 * np.pi * (self.collimator_radius ** 2) / (self.distance ** 2)

    def g_constant(self, angles: np.ndarray) -> np.ndarray:
        x2 = self.x_square()
        angles_in_rad = angles * np.pi / 180

        numerator = np.sqrt(1 - x2 * (np.sin(angles_in_rad) ** 2))
        denumerator = (np.sqrt(x2) * np.cos(angles_in_rad) + numerator) ** 2

        return numerator / denumerator

    def x_square(self) -> float:
        const = (self.a * self.b) / (self.A * self.B)
        brackets = 1 + (1 + self.a / self.A) * self.reaction_q / self.beam_energy

        return const / brackets
    