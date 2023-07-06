import threading
import numpy as np

from business.physics import Reaction, Nuclei, Struggling
from business.electronics import Detector, Telescope


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

    def stop_energy_losses(self, reaction: Reaction, angle: float) -> dict[Nuclei, np.ndarray]:
        de_losses = self.de_energy_losses(reaction, angle)
        after_reactions = self.__ear_range(reaction, angle)

        quits = after_reactions[:len(de_losses)] - de_losses

        material = self.telescope.e_detector.madeof_nuclei
        dx = self.telescope.e_detector.thickness
        ro = self.telescope.e_detector.density

        bethe_bloch = Struggling(reaction.fragment, material)

        loses = bethe_bloch.energy_loss(quits, dx, ro)
        loses[loses > quits] = quits[loses > quits]

        return loses

    def de_energy_losses(self, reaction: Reaction, angle: float) -> np.ndarray:
        quits = self.__ear_range(reaction, angle)

        material = self.telescope.de_detector.madeof_nuclei
        dx = self.telescope.de_detector.thickness
        ro = self.telescope.de_detector.density

        bethe_bloch = Struggling(reaction.fragment, material)

        loses = bethe_bloch.energy_loss(quits, dx, ro)
        loses[loses > quits] = 0

        return loses
    
    def __ear_range(self, reaction: Reaction, angle: float) -> np.ndarray:
        maximum = reaction.fragment_energy(reaction.residual.states[0], angle)
        minimum = maximum

        for i in range(1, len(reaction.residual.states)):
            current_state = reaction.residual.states[i]

            if reaction.reaction_quit(current_state) + reaction.cm_energy() <= 0:
                break
            minimum = min(reaction.fragment_energy(current_state, angle), minimum)

        return np.linspace(minimum, maximum, 50)

    def possible_reactions(self) -> list[Reaction]:
        hypotetic = [Reaction(self.beam, self.target, one, self.beam_energy) for one in self.POSSIBLE_PARTICLES]
        return [react for react in hypotetic if react.cm_energy() + react.reaction_quit() >= 0]


if __name__ == '__main__':
    pass
