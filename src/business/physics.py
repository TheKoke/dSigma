from __future__ import annotations

import numpy as np
from business.consts import MASS_EXCESSES, STATES, WIGNER_WIDTHS


class Nuclei:
    def __init__(self, charge: int, nuclons: int) -> None:
        self.nuclons = nuclons
        self.charge = charge

    @property
    def mass_excess(self) -> float:
        return MASS_EXCESSES[(self.charge, self.nuclons)]
    
    @property
    def states(self) -> list[float]:
        return STATES[(self.charge, self.nuclons)]
    
    @property
    def wigner_widths(self) -> list[float]:
        return WIGNER_WIDTHS[(self.charge, self.nuclons)]
    
    @property
    def radius(self) -> float:
        fermi = 1.28e-13 # cm
        return fermi * np.cbrt(self.nuclons) # cm
    
    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        return f'Nuclei(Z: {self.charge}, A: {self.nuclons})'
    
    def __eq__(self, other: Nuclei) -> bool:
        return self.nuclons == other.nuclons and self.charge == other.charge
    
    def __add__(self, other: Nuclei) -> Nuclei:
        return Nuclei(self.charge + other.charge, self.nuclons + other.nuclons)
    
    def __sub__(self, other: Nuclei) -> Nuclei:
        return Nuclei(self.charge - other.charge, self.nuclons - other.nuclons)
    
    def mass(self, unit: str = 'MeV') -> float:
        match unit.lower():
            case 'mev': 
                return self.charge * 938.27 + (self.nuclons - self.charge) * 939.57
            case 'amu' | 'a.m.u':
                return self.charge * 1.007276467 + (self.nuclons - self.charge) * 1.008664915
            case 'g':
                return self.charge * 1.672e-24 + (self.nuclons - self.charge) * 1.675e-24
            case _:
                return self.nuclons


class Reaction:
    def __init__(self, beam: Nuclei, target: Nuclei, fragment: Nuclei, beam_energy: float) -> None:
        self.beam = beam
        self.target = target
        self.fragment = fragment
        self.residual = self.__residual_nuclei()

        self.beam_energy = beam_energy

    @property
    def is_elastic(self) -> bool:
        return self.beam == self.fragment
    
    def __eq__(self, other: Reaction) -> bool:
        return self.beam == other.beam \
            and self.target == other.target \
            and self.fragment == other.fragment \
            and self.beam_energy == other.beam_energy

    def __residual_nuclei(self) -> Nuclei:
        return self.beam + self.target - self.fragment

    def reaction_quit(self, residual_state: float = 0) -> float:
        q0 = (self.beam.mass_excess + self.target.mass_excess) - (self.fragment.mass_excess + self.residual.mass_excess)
        return q0 - residual_state
    
    def reaction_threshold(self, residual_state: float = 0) -> float:
        if self.reaction_quit(residual_state) > 0:
            return self.couloumb_potential()

        brackets = 1 + (self.beam.mass() / self.target.mass())
        brackets += (abs(self.reaction_quit(residual_state)) / (2 * self.target.mass()))

        return abs(self.reaction_quit(residual_state)) * brackets
    
    def cm_energy(self) -> float:
        to_system = self.beam.mass() / (self.beam.mass() + self.target.mass()) * self.beam_energy
        return self.beam_energy - to_system
    
    def fragment_energy(self, residual_state: float, fragment_angle: float) -> float:
        r = Reaction.__r_factor(
            self.beam.mass(), 
            self.beam_energy, 
            self.fragment.mass(), 
            self.residual.mass(), 
            fragment_angle * np.pi / 180
        )

        s = Reaction.__s_factor(
            self.beam.mass(), 
            self.beam_energy, 
            self.fragment.mass(), 
            self.residual.mass(), 
            self.reaction_quit(residual_state)
        )

        return (r + np.sqrt(r ** 2 + s)) ** 2
    
    def residual_energy(self, residual_state: float) -> float:
        r = Reaction.__r_factor(
            self.beam.mass(),
            self.beam_energy, 
            self.residual.mass(),
            self.fragment.mass(),
            self.residual_angle(residual_state)
        )

        s = Reaction.__s_factor(
            self.beam.mass(),
            self.beam_energy,
            self.residual.mass(),
            self.fragment.mass(),
            self.reaction_quit(residual_state)
        )

        return (r + np.sqrt(r ** 2 + s)) ** 2
    
    def residual_angle(self, residual_state: float, fragment_angle: float) -> float:
        fragment_ears = self.fragment_energy(residual_state, fragment_angle)
        energy_relation = np.sqrt(self.beam.mass() * self.beam_energy / (self.fragment.mass() * fragment_ears))

        return np.pi / 2 - np.arctan(
            (energy_relation - np.cos(fragment_angle * np.pi / 180)) / np.sin(fragment_angle * np.pi / 180)
        )
    
    @staticmethod
    def __r_factor(beam_mass: float, beam_energy: float, 
                   instance_mass: float, partner_mass: float, angle: float) -> float:
        numerator = np.sqrt(beam_mass * instance_mass * beam_energy) * np.cos(angle)
        return numerator / (instance_mass + partner_mass)

    @staticmethod
    def __s_factor(beam_mass: float, beam_energy: float, 
                   instance_mass: float, partner_mass: float, reaction_quit: float) -> float:
        numerator = beam_energy * (partner_mass - beam_mass) + partner_mass * reaction_quit
        return numerator / (instance_mass + partner_mass)
    
    def grazing_angle(self) -> float:
        E = self.cm_energy()
        V = self.couloumb_potential()
        return 2 * np.arcsin(V / (2 * E - V)) * 180 / np.pi

    def couloumb_potential(self) -> float:
        reduced_planck = 6.582e-22 # MeV * s
        lightspeed = 3e10 # cm / s
        fine_structure = 1 / 137 # dimensionless

        e_power_2 = fine_structure * reduced_planck * lightspeed
        effective_radius = self.beam.radius + self.target.radius + 2e-13
        return self.beam.charge * self.target.charge * e_power_2 / effective_radius
    
    def rutherford_scattering(self) -> np.ndarray:
        angle_range = np.arange(1, 179) * np.pi / 180 # rad
        reduced_planck = 6.582e-22 # MeV * s
        lightspeed = 3e10 # cm / s
        fine_structure = 1 / 137 # dimensionless

        e_power_2 = fine_structure * reduced_planck * lightspeed
        numerator = self.beam.charge * self.target.charge * e_power_2 # MeV * cm
        denumerator = 4 * self.beam_energy * np.sin(angle_range / 2) ** 2 # MeV * rad

        return np.power(numerator / denumerator, 2) * 1e24 # cm^2 / rad^2  => barn / srad
    

class Struggling:
    def __init__(self, stray: Nuclei, environ: Nuclei) -> None:
        self.stray = stray
        self.environ = environ

    def energy_loss(self, energy: float, thickness: float, ro: float) -> None:
        return self.specific_energy_loss(energy, ro) * thickness
    
    def specific_energy_loss(self, energy: float, ro: float) -> float:
        electron_mass = 0.511 # MeV
        reduced_planck = 6.582e-22 # MeV * s
        lightspeed = 3e10 # cm / s
        fine_structure = 1 / 137 # dimensionless

        e_power_4 = (reduced_planck * lightspeed * fine_structure) ** 2 # MeV^2 * cm^2
        betta_power_2 = self.lorenz_parameter(energy) ** 2 # dimensionless

        common = 4 * np.pi * self.electrons_density(ro) * self.stray.charge ** 2
        common *= e_power_4 / (electron_mass * betta_power_2)

        logarithm = np.log(2 * electron_mass * betta_power_2 / self.mean_environ_excitation())
        relativistic = np.log(1 - betta_power_2) + betta_power_2

        return common * (logarithm - relativistic) # MeV * cm^-1

    def mean_environ_excitation(self) -> float:
        hydrogen_ionization = 13.6e-6 # MeV
        return hydrogen_ionization * self.environ.charge
    
    def electrons_density(self, ro: float) -> float:
        avogadro = 6.02e23 # mol^-1
        return self.environ.charge * ro * avogadro / self.environ.nuclons # electrons * cm^-3
    
    def lorenz_parameter(self, energy: float) -> float:
        #  dimensionless     MeV          MeV        
        return np.sqrt(2 * energy / self.stray.mass())


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


class PhysicalExperiment:
    def __init__(self, beam: Nuclei, target: Nuclei, beam_energy: float) -> None:
        self.__beam = beam
        self.__target = target
        self.__beam_energy = beam_energy

    @property
    def beam(self) -> Nuclei:
        return self.__beam
    
    @property
    def target(self) -> Nuclei:
        return self.__target
    
    @property
    def beam_energy(self) -> float:
        return self.__beam_energy

    def create_reaction(self, fragment: Nuclei) -> Reaction:
        compound = self.__beam + self.__target
        if fragment.charge > compound.charge:
            raise ValueError('Ejectile particle greater than reaction components.')
        
        hypotese = Reaction(self.__beam, self.__target, fragment, self.__beam_energy)
        if hypotese.reaction_threshold() > self.__beam_energy:
            raise ValueError('Energy of beam is not enough for produce reaction.')

        return hypotese


if __name__ == '__main__':
    pass
