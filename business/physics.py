import numpy as np
from isotopes import *


class Nuclei:
    def __init__(self, nuclons: int, charge: int) -> None:
        self.nuclons = nuclons
        self.charge = charge
        self.mass_excess = self.__mass_excess()

    def __mass_excess(self) -> float:
        return deltaM[(self.charge, self.nuclons)]

    def mass(self, unit: str = 'MeV') -> float:
        return self.charge * 938.27 + (self.nuclons - self.charge) * 939.57


class Reaction:
    def __init__(self, beam: Nuclei, target: Nuclei, fragment: Nuclei, beam_energy: float, angle: float) -> None:
        self.beam = beam
        self.target = target
        self.fragment = fragment
        self.residual = self.__residual_nuclei()

        self.beam_energy = beam_energy
        self.angle = angle * np.pi / 180

    def __residual_nuclei(self) -> Nuclei:
        nuclon = (self.beam.nuclons + self.target.nuclons) - self.fragment.nuclons
        charge = (self.beam.charge + self.target.charge) - self.fragment.charge
        return Nuclei(nuclon, charge)

    def reaction_quit(self, residual_state: float = 0) -> float:
        q0 = (self.beam.mass_excess + self.target.mass_excess) - (self.fragment.mass_excess + self.residual.mass_excess)
        return q0 - residual_state
    
    def fragment_energy(self, residual_state: float) -> float:
        r = self.r_const()
        s = self.s_const(residual_state)

        return (r + np.sqrt(r ** 2 + s)) ** 2

    def r_const(self) -> float:
        numerator = np.sqrt(self.beam.mass() * self.fragment.mass() * self.beam_energy) * np.cos(self.angle)
        return numerator / (self.fragment.mass() + self.residual.mass())

    def s_const(self, residual_state: float) -> float:
        numerator = self.beam_energy * (self.residual.mass() - self.beam.mass()) + self.residual.mass() * self.reaction_quit(residual_state)
        return numerator / (self.fragment.mass() + self.residual.mass())

    #TODO: implement this method. Note: minimalizing the energy
    def residual_collapse(self) -> tuple[Nuclei, Nuclei]:
        if self.residual.nuclons == 6 and self.residual.charge == 3:
            return (Nuclei(4, 2), Nuclei(2, 1))


if __name__ == '__main__':
    pass
