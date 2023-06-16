from __future__ import annotations

import numpy as np
from consts import *


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

    def __str__(self) -> str:
        return f'A: {self.nuclons}, Z: {self.charge}'
    
    def __eq__(self, __o: Nuclei) -> bool:
        return self.nuclons == __o.nuclons and self.charge == __o.charge
    
    def __add__(self, __o: Nuclei) -> Nuclei:
        return Nuclei(self.nuclons + __o.nuclons, self.charge + __o.charge)
    
    def mass(self, unit: str = 'MeV') -> float:
        if unit == 'MeV':
            return self.charge * 938.27 + (self.nuclons - self.charge) * 939.57
        
        if unit == 'a.m.u.':
            return self.charge * 1.007276467 + (self.nuclons - self.charge) * 1.008664915
        
        if unit == 'g':
            return self.charge * 1.672e-24 + (self.nuclons - self.charge) * 1.675e-24


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

    def __residual_nuclei(self) -> Nuclei:
        nuclon = (self.beam.nuclons + self.target.nuclons) - self.fragment.nuclons
        charge = (self.beam.charge + self.target.charge) - self.fragment.charge
        return Nuclei(charge, nuclon)

    def reaction_quit(self, residual_state: float = 0) -> float:
        q0 = (self.beam.mass_excess + self.target.mass_excess) - (self.fragment.mass_excess + self.residual.mass_excess)
        return q0 - residual_state
    
    def reaction_threshold(self, residual_state: float = 0) -> float:
        brackets = 1 + (self.beam.mass() / self.target.mass())
        brackets += (abs(self.reaction_quit(residual_state)) / (2 * self.target.mass()))

        return abs(self.reaction_quit(residual_state)) * brackets
    
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
    

class Ionization:
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

        e_power_4 = (reduced_planck * lightspeed * fine_structure) ** 2
        betta_power_2 = self.lorenz_parameter(energy) ** 2

        common = 4 * np.pi * self.electrons_density(ro) * self.stray.charge ** 2
        common *= e_power_4 / (electron_mass * betta_power_2)

        logarithm = np.log(2 * electron_mass * betta_power_2 / self.mean_environ_excitation())
        relativistic = np.log(1 - betta_power_2) + betta_power_2

        return common * (logarithm - relativistic) # MeV * sm^-1

    def mean_environ_excitation(self) -> float:
        hydrogen_ionization = 13.6e-6 # MeV
        return hydrogen_ionization * self.environ.charge
    
    def electrons_density(self, ro: float) -> float:
        avogadro = 6.02e23 # mol^-1
        return self.environ.charge * ro * avogadro / self.environ.nuclons # electrons * sm^-3
    
    def lorenz_parameter(self, energy: float) -> float:
        #  dimensionless     MeV          MeV        
        return np.sqrt(2 * energy / self.stray.mass())


if __name__ == '__main__':
    pass
