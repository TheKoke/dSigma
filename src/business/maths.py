import numpy as np
from business.physics import Reaction
from scipy.optimize import curve_fit

class Gaussian:
    def __init__(self, xy: np.ndarray, fwhm: np.float64) -> None:
        self.xdata = xy[0]
        self.ydata = xy[1]

        self.peak_index = len(self.xdata) // 2
        self.peak_center = self.xdata[self.peak_index]
        self.fwhm = fwhm

        self.area = self.__area()

    def to_workbook(self) -> str:
        pass

    def __str__(self, /, dispersion_view: bool = False, fwhm_view: bool = True) -> str:
        func = 'G(x) = '

        if dispersion_view:
            func += f'{np.round(self.area, 3)} / (sqrt(2pi * {np.round(self.dispersion(), 3)}) * ' \
                    f'exp(-(x - {np.round(self.peak_center, 3)})^2 / 2{np.round(self.dispersion(), 3)})'

        if fwhm_view:
            func += f'{np.round(self.area, 3)} / ({np.round(self.fwhm, 3)} * sqrt(pi / 4ln2)) * ' \
                    f'exp(- 4ln2 * (x - {np.round(self.peak_center, 3)})^2 / {np.round(self.fwhm ** 2, 3)}))'

        return func

    def __area(self) -> np.float64:
        def gauss(x, a):
            return (a / (self.fwhm * np.sqrt(np.pi / (4 * np.log(2))))) * np.exp(-1 * (4 * np.log(2))
            / (self.fwhm ** 2) * (x - self.peak_center) ** 2)

        parameters = curve_fit(gauss, self.xdata, self.ydata)

        return parameters[0][0]
    
    def refresh_area(self) -> float:
        self.area = self.__area()
        return self.area

    def dispersion(self) -> np.float64:
        return self.fwhm / (2 * np.sqrt(2 * np.log(2)))

    def three_sigma(self) -> np.ndarray:
        return np.linspace(-3 * self.dispersion() + self.peak_center, 3 * self.dispersion() + self.peak_center, 50)

    def function(self) -> np.ndarray:
        constant = self.area / (self.fwhm * np.sqrt(np.pi / (4 * np.log(2))))
        exp_constant = -1 * (4 * np.log(2)) / (self.fwhm ** 2)

        array_part = (self.three_sigma() - self.peak_center) ** 2

        return constant * np.exp(exp_constant * array_part)


class Parabola:
    def __init__(self, slope: float, shift: float) -> None:
        self.slope = slope
        self.shift = shift

    def __str__(self) -> str:
        return f'y = {self.slope}sqrt({self.shift} - x)'

    def values(self, args: np.ndarray) -> np.ndarray:
        return self.slope * np.sqrt(self.shift - args)


class CrossSection:
    def __init__(self, reaction: Reaction) -> None:
        '''
        cross_section for reaction
        A(a, b)B
        '''

        self.A = reaction.target.nuclons; self.a = reaction.beam.nuclons
        self.B = reaction.residual.nuclons; self.b = reaction.fragment.nuclons

        self.integrator_const = 1e-6
        self.norm = 1

        self.distance = 200
        self.collimator_radius = 1.6

        self.target_concentrate = 1
        self.target_thickness = 1

        self.reaction_q = reaction.reaction_quit()
        self.beam_energy = reaction.beam_energy

    def set_geometrical_parameters(self, distance: float, collimator_radius: float) -> None:
        self.distance = distance
        self.collimator_radius = collimator_radius

    def set_target_properties(self, concentrate: float, thickness: float) -> None:
        self.target_concentrate = concentrate
        self.target_thickness = thickness

    def set_electronics(self, integrator_const: float, norm: float) -> None:
        self.integrator_const = integrator_const
        self.norm = norm
    
    def formula(self, events: np.ndarray, angles: np.ndarray, integrator: np.ndarray, misscalculation: np.ndarray) -> np.ndarray:
        numerator = self.A * events * misscalculation * self.norm
        denumerator = integrator * self.integrator_const * self.target_concentrate * self.target_thickness * self.solid_angle()

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
    