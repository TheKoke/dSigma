import numpy as np
from spectr import Spectr

class Equipment:
    def __init__(self, concentrate: np.float64, diff_thick: np.float64,
    A: np.float64, a: np.float64, b: np.float64, B: np.float64) -> None:
        self.concentrate = concentrate
        self.diff_thick = diff_thick

        self.A = A
        self.a = a
        self.b = B
        self.B = b

        self.reaction_energy = 0
        self.ion_kinetic = 0

    def set_energies(self, reaction: np.float64, ion: np.float64) -> None:
        self.reaction_energy = reaction
        self.ion_kinetic = ion

class CrossSection:
    def __init__(self, spectr: Spectr, eqp: Equipment, angles: np.ndarray, 
    norm: np.float64, misscalc: np.float64, integrator_count: np.ndarray,
    integrator_const: np.float64, distance: np.float64, kollimator_radius: np.float64) -> None:

        self.states = spectr.peaks
        self.areas = spectr.calc_areas()
        self.angles = angles
        self.norm = norm

        self.eqp = eqp

        self.misscalc = misscalc
        self.intg_count = integrator_count
        self.intg_constant = integrator_const

        self.dist = distance
        self.koll_radius = kollimator_radius

    def solid_ange(self) -> np.float64:
        return 2 * np.pi * self.koll_radius ** 2 / (self.dist ** 2)

    def laboratory_cross(self) -> np.ndarray:
        numerator = self.areas * self.eqp.A * self.misscalc * self.norm
        denum = self.intg_count * self.intg_constant * self.solid_ange() * self.eqp.concentrate * self.eqp.diff_thick

        return numerator / denum

    def center_mass_cross(self) -> np.ndarray:
        return self.__g_constant() * self.laboratory_cross()

    def to_workbook(self) -> np.ndarray:
        pass

    def cm_angles(self) -> np.ndarray:
        pass

    def __g_constant(self) -> np.float64:
        pass

    def __x_square(self) -> np.float64: 
        const = (self.eqp.a * self.eqp.b) / (self.eqp.A * self.eqp.B) 
        brackets = 1 + (1 + self.eqp.a / self.eqp.A) * self.eqp.reaction_energy / self.eqp.ion_kinetic

        return const * 1 / brackets