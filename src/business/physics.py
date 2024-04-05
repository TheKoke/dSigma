from __future__ import annotations

import numpy as np
from business.informer import Informator, NAME2CHARGE


class Nuclei:
    def __init__(self, charge: int, nuclons: int) -> None:
        if not Informator.is_exist(charge, nuclons):
            raise ValueError(f'Not such a nuclei with z={charge} and a={nuclons}')

        self.nuclons = nuclons
        self.charge = charge
        self.name = Informator.name(self.charge, self.nuclons)

    @property
    def mass_excess(self) -> float:
        return Informator.mass_excess(self.charge, self.nuclons)
    
    @property
    def states(self) -> list[float]:
        return Informator.states(self.charge, self.nuclons)
    
    @property
    def spins(self) -> list[tuple[float, bool]]:
        return Informator.spins(self.charge, self.nuclons)
    
    @property
    def wigner_widths(self) -> list[float]:
        return Informator.wigner_widths(self.charge, self.nuclons)
    
    @property
    def radius(self) -> float:
        fermi = 1.28e-13 # cm
        return fermi * np.cbrt(self.nuclons) # cm
    
    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
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
            
    @staticmethod
    def from_string(input: str) -> Nuclei:
        if Nuclei.handle_human_namings(input) is not None:
            return Nuclei.handle_human_namings(input)

        only_name = ''.join([i.lower() for i in input if i.isalpha()])
        only_nuclons = ''.join([i for i in input if i.isdigit()])

        charge = NAME2CHARGE[only_name]
        nuclon = int(only_nuclons)
        
        return Nuclei(charge, nuclon)
    
    @staticmethod
    def handle_human_namings(input: str) -> Nuclei:
        if input in ['p', 'd', 't']:
            return Nuclei(1, ['p', 'd', 't'].index(input) + 1)
        
        if input == 'alpha' or input == 'α' or input == 'a':
            return Nuclei(2, 4)
        
        return None


class Reaction:
    def __init__(self, beam: Nuclei, target: Nuclei, fragment: Nuclei, beam_energy: float) -> None:
        self.beam = beam
        self.target = target
        self.fragment = fragment
        self.beam_energy = beam_energy

        self.residual = self.__residual_nuclei()
        self.residual_states = self.__residual_states()

    @property
    def is_elastic(self) -> bool:
        return self.beam == self.fragment
    
    def __eq__(self, other: Reaction) -> bool:
        return self.beam == other.beam \
            and self.target == other.target \
            and self.fragment == other.fragment \
            and self.beam_energy == other.beam_energy
    
    def __repr__(self) -> str:
        return f'{self.target}({self.beam}, {self.fragment}){self.residual}'
    
    def __str__(self) -> str:
        return f'{self.target}({self.beam}, {self.fragment}){self.residual}'

    def __residual_nuclei(self) -> Nuclei:
        return self.beam + self.target - self.fragment
    
    def __residual_states(self) -> list[float]:
        all_states = self.residual.states

        possible = []
        for state in all_states:
            if self.reaction_threshold(state) > self.beam_energy:
                break
            
            possible.append(state)

        return possible

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
    def __init__(self, reaction: Reaction, angle_range: np.ndarray) -> None:
        '''
        Differential cross section for reaction.
        '''
        self.reaction = reaction
        self.angle_range = angle_range

        self.__values = {state: np.zeros_like(self.angle_range) for state in self.reaction.residual_states}

    @property
    def values(self) -> dict[float, np.ndarray]:
        return self.__values.copy()
    
    def to_workbook(self) -> str:
        angles = self.angle_to_cm()
        report = f'Differential cross-section of {self.reaction} reaction at {self.reaction.beam_energy} MeV energy.\n\n'
        
        for state in self.__values:
            report += f'Values for {state}(spin) MeV excitation state of {self.reaction.residual}->\n' # add spin text.
            report += 'c.m. angle, deg.'.center(30) + '\t|\t' + 'diff.c.s., mb/sr'.center(30) + '\n'
            for i in range(len(self.__values[state])):
                report += str(round(angles[i], 3)).center(30) + '\t\t' + str(round(self.__values[state][i], 3)).center(30) + '\n'

            report += '\n\n'

        return report
    
    def angle_to_cm(self) -> np.ndarray:
        x2 = np.sqrt(self.x_square())
        angles_in_rad = self.angle_range * np.pi / 180

        multiplier = (x2 * np.sin(angles_in_rad)) ** 2

        return np.arctan(np.sqrt(multiplier) / np.sqrt(1 - multiplier)) * 180 / np.pi + self.angle_range
    
    def cm_cross_section_of(self, state: float) -> np.ndarray:
        lab_dsigma = self.lab_cross_section_of(state)
        return lab_dsigma * self.g_constant()[:len(lab_dsigma)]
    
    def g_constant(self) -> np.ndarray:
        x2 = self.x_square()
        angles_in_rad = self.angle_range * np.pi / 180

        numerator = np.sqrt(1 - x2 * (np.sin(angles_in_rad) ** 2))
        denumerator = (np.sqrt(x2) * np.cos(angles_in_rad) + numerator) ** 2

        return numerator / denumerator

    def x_square(self) -> float:
        a = self.reaction.beam.nuclons
        b = self.reaction.fragment.nuclons
        A = self.reaction.target.nuclons
        B = self.reaction.residual.nuclons

        const = (a * b) / (A * B)
        brackets = 1 + (1 + a / A) * self.reaction.reaction_quit() / self.reaction.beam_energy

        return const / brackets

    def lab_cross_section_of(self, state: float) -> np.ndarray:
        if state not in self.reaction.residual_states:
            raise ValueError(f'Residual nuclei does not have state with excited energy: {state} MeV.')
        
        return self.__values[state]
        
    def add_cross_section_for(self, state: float, sigmas: np.ndarray) -> None:
        if state not in self.reaction.residual_states:
            raise ValueError(f'Residual nuclei does not have state with excited energy: {state} MeV.')
        
        self.__values[state] = sigmas


class PhysicalExperiment:
    def __init__(self, beam: Nuclei, target: Nuclei, beam_energy: float) -> None:
        self.beam = beam
        self.target = target
        self.beam_energy = beam_energy

    def possible_channels(self) -> list[Reaction]:
        queue = [Nuclei(0, 1), Nuclei(1, 1), Nuclei(1, 2), Nuclei(1, 3), Nuclei(2, 3), Nuclei(2, 4)]
        if self.beam in queue:
            queue = queue[:queue.index(self.beam) + 1]

        elastic = Reaction(self.beam, self.target, self.beam, self.beam_energy)
        current = None
        
        pick_up = []
        for i in queue:
            try:
                current = self.create_reaction(self.beam - i)
                pick_up.append(current)
            except:
                continue

        stripped = []
        for i in queue:
            try:
                current = self.create_reaction(self.beam + i)
                stripped.append(current)
            except:
                continue

        return pick_up + [elastic] + stripped

    def create_reaction(self, fragment: Nuclei) -> Reaction:
        compound = self.beam + self.target
        if fragment.charge > compound.charge:
            raise ValueError('Ejectile particle greater than reaction components.')
        
        hypotese = Reaction(self.beam, self.target, fragment, self.beam_energy)
        if hypotese.reaction_threshold() > self.beam_energy:
            raise ValueError('Energy of beam is not enough for produce reaction.')

        return hypotese


if __name__ == '__main__':
    pass
