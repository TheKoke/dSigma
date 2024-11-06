import numpy
import multiprocessing

from business.locus import Locus
from business.auto.slice import Slicer
from business.auto.density import DensityMatrix
from business.auto.searching import Beagle, Pinnacle


class Identifier:
    def __init__(self, matrix: numpy.ndarray) -> None:
        self.matrix = matrix
        self._processed = numpy.array([])

    @property
    def processed_matrix(self) -> numpy.ndarray:
        if len(self._processed) == 0:
            # Double densed with first step zero encounting limiting.
            one_densed = DensityMatrix(self.matrix, zero_encount_limit=0)
            two_densed = DensityMatrix(one_densed.density)
            self._processed = two_densed.density.copy()

            mean = self._processed.sum() / (len(self.processed_matrix) ** 2)
            self._processed[self._processed < mean] = 0

        return self._processed.copy()
    
    @property
    def order(self) -> int:
        bins = len(self.matrix)
        n = 0
        while bins > 0:
            bins //= 2
            n += 1
        return n

    def build_locuses(self) -> list[Locus]:
        families = self.handle_families()
        with multiprocessing.Pool(len(families)) as pool:
            return pool.map(self.borders_to_locus, families)
        
    def borders_to_locus(self, pinnacles: dict[int, Pinnacle]) -> Locus:
        ceil = []
        floor = []
        for ch in pinnacles:
            ceil.append((ch, pinnacles[ch].right))
            floor.append((ch, pinnacles[ch].left))

        ceil[0] = (ceil[0][0] - self.order // 2, ceil[0][1])
        ceil[-1] = (ceil[-1][0] + self.order // 2, ceil[-1][1])
        floor[0] = (floor[0][0] - self.order // 2, floor[0][1])
        floor[-1] = (floor[-1][0] + self.order // 2, floor[-1][1])

        floor.reverse()
        points = ceil + floor + [ceil[0]]

        return Locus(self.matrix, points)
    
    def handle_families(self) -> list[dict[int, Pinnacle]]:
        pinns = self.collect_pinnacles()

        families: list[dict[int, Pinnacle]] = []
        family_gammas: list[float] = []

        for channel in pinns:
            for pinn in pinns[channel]:
                e_value = channel
                de_value = pinn.center

                gamma = self.gamma(e_value, de_value)
                is_new_locus = self.is_new_locus(family_gammas, gamma)

                if is_new_locus:
                    families.append({channel: pinn})
                    family_gammas.append(gamma)
                else:
                    closest = numpy.argmin(numpy.abs(numpy.array(family_gammas) - gamma))
                    family_gammas[closest] = gamma
                    families[closest][channel] = pinn

        return families
    
    def gamma(self, e_channel: int, de_channel: int) -> float:
        return 1.745 * (0.0003 * e_channel + de_channel) * (e_channel + 0.472 * de_channel) ** (0.73)
    
    def is_new_locus(self, families: list[float], gamma: float) -> bool:
        pretend_exponent = int(numpy.log10(gamma))
        pretend_mantissa = int(gamma / numpy.power(10, pretend_exponent))

        flag = True
        for i in range(len(families)):
            current_exponent = int(numpy.log10(families[i]))
            current_mantissa = int(families[i] / numpy.power(10, current_exponent))

            is_close = current_exponent == pretend_exponent and abs(current_mantissa - pretend_mantissa) <= 1
            is_close = is_close and gamma <= families[i]
            flag = flag and not is_close

        return flag
    
    def collect_pinnacles(self) -> dict[int, list[Pinnacle]]:
        THREADS = 8

        slicer = Slicer()
        slices = slicer.shred(self.processed_matrix, step=self.order)

        with multiprocessing.Pool(THREADS) as pool:
            n = len(slices.keys())
            chunks = []

            for i in range(THREADS):
                chunks.append(dict())
                for _ in range(n // THREADS):
                    ch, sl = slices.popitem()
                    chunks[i][ch] = sl
            
            for _ in range(n - THREADS * (n // THREADS)):
                ch, sl = slices.popitem()
                chunks[-1][ch] = sl

            pinns = pool.map(self.find_pinnacles, chunks)

        copy = dict()
        for chunk in pinns:
            copy = copy | chunk
        return dict(sorted(copy.items()))

    def find_pinnacles(self, slices: dict[int, numpy.ndarray]) -> dict[int, Pinnacle]:
        pinns = dict()
        for channel in slices:
            searcher = Beagle(slices[channel])
            pinns[channel] = searcher.peaks()

        return pinns
    

if __name__ == '__main__':
    pass
