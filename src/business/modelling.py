import threading
import numpy as np

from business.physics import Reaction, Nuclei, Ionization
from business.electronics import Telescope


class Modelier:
    POSSIBLE_PARTICLES = [
        Nuclei(1, 1), # proton
        Nuclei(1, 2), # deuteron
        Nuclei(1, 3), # triton
        Nuclei(2, 3), # helion, He-3
        Nuclei(2, 4), # alpha, He-4
    ]

    def __init__(self, beam: Nuclei, target: Nuclei, beam_energy: float, telescope: Telescope) -> None:
        self.beam = beam
        self.target = target
        self.beam_energy = beam_energy

        self.telescope = telescope

    def fill(self, angle: float) -> np.ndarray:
        e_de = np.ones((self.telescope.e_binning, self.telescope.de_binning))

    def stopped_energy(self, reaction: Reaction, de_losses: np.ndarray, angle: float) -> np.ndarray:
        after_reactions = self.__after_reaction_energies_range(reaction, angle)
        quits = after_reactions[len(after_reactions) - len(de_losses):] - de_losses

        material = self.telescope.e_detector.madeof_nuclei
        dx = self.telescope.e_detector.thickness
        ro = self.telescope.e_detector.density

        bethe_bloch = Ionization(reaction.fragment, material)
        struggled = bethe_bloch.energy_loss(quits, dx, ro)

        struggled[struggled > quits] = quits[struggled > quits]
        return struggled

    def de_energy_losses(self, reaction: Reaction, angle: float) -> np.ndarray:
        quits = self.__after_reaction_energies_range(reaction, angle)

        material = self.telescope.de_detector.madeof_nuclei
        dx = self.telescope.de_detector.thickness
        ro = self.telescope.de_detector.density

        bethe_bloch = Ionization(reaction.fragment, material)
        struggled = bethe_bloch.energy_loss(quits, dx, ro)

        struggled[struggled > quits] = 0
        return np.delete(struggled, np.argwhere(struggled <= 0))
    
    def __after_reaction_energies_range(self, reaction: Reaction, angle: float) -> np.ndarray:
        maximum = reaction.fragment_energy(0, angle)
        minimum = 0.1

        return np.linspace(minimum, maximum, 100)

    def possible_reactions(self) -> list[Reaction]:
        hypotetic = [Reaction(self.beam, self.target, one, self.beam_energy) for one in self.POSSIBLE_PARTICLES]
        return [react for react in hypotetic if react.cm_energy() + react.reaction_quit() >= 0]


if __name__ == '__main__':
    pass
