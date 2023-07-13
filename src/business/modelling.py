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
        graphs = self.collect_bethes(angle)
        matrixes = [np.zeros((self.telescope.e_binning, self.telescope.de_binning))] * len(graphs)

        threads = []
        for i in range(len(graphs)):
            threads.append(threading.Thread(target=self.smash, args=[graphs, matrixes[i]]))
            threads[-1].start()

        for t in threads:
            t.join()

        final = np.zeros_like(matrixes[0])
        for matrix in matrixes:
            final = final + matrix

        del threads
        return final

    def smash(self, graph: np.ndarray, destination: np.ndarray) -> None:
        pass

    def collect_bethes(self, angle: float) -> list[np.ndarray]:
        reactions = self.possible_reactions()
        threads = []
        result = [np.array([])] * len(reactions)

        for i in range(len(reactions)):
            threads.append(threading.Thread(target=self.energy_losses, args=[reactions[i], angle, result[i]]))
            threads[-1].start()

        for t in threads:
            t.join()

        del threads
        return result

    def energy_losses(self, reaction: Reaction, angle: float, destination: np.ndarray) -> None:
        de_losses = self.de_energy_losses(reaction, angle)
        after_reactions = self.__ear_range(reaction, angle)

        quits = after_reactions[:len(de_losses)] - de_losses

        material = self.telescope.e_detector.madeof_nuclei
        dx = self.telescope.e_detector.thickness
        ro = self.telescope.e_detector.density

        bethe_bloch = Struggling(reaction.fragment, material)

        losses = bethe_bloch.energy_loss(quits, dx, ro)
        losses[losses > quits] = quits[losses > quits]

        destination = np.vstack((de_losses, losses))

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
        return [react for react in hypotetic if react.beam_energy > react.reaction_threshold()]


if __name__ == '__main__':
    pass
