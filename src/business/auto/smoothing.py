import numpy


class QH353:
    def __init__(self) -> None:
        pass

    def smooth(self, spectrum: numpy.ndarray) -> numpy.ndarray:
        z = spectrum.copy()

        z = self.running_median(z, 3)
        z = self.running_median(z, 5)
        z = self.running_median(z, 3)
        z = self.running_average(z)
        r = self.residual_smooth(spectrum, z)

        return (z + r).astype(numpy.int32)

    def running_median(self, spectrum: numpy.ndarray, n: int = 3) -> numpy.ndarray:
        runned = spectrum.copy()

        for i in range(n // 2, len(spectrum) - n // 2):
            runned[i] = self._median_of(spectrum[i - n // 2: i + n // 2 + 1])

        if n == 3:
            seq = numpy.array([spectrum[0], runned[1], 3 * runned[1] - 2 * runned[2]])
            runned[0] = self._median_of(seq)

            seq = numpy.array([spectrum[-1], runned[-2], 3 * runned[-2] - 2 * runned[-3]])
            runned[-1] = self._median_of(seq)

        if n == 5:
            seq = numpy.array([spectrum[0], spectrum[1], spectrum[2]])
            runned[1] = self._median_of(seq)

            seq = numpy.array([spectrum[-3], spectrum[-2], spectrum[-1]])
            runned[-2] = self._median_of(seq)
        
        return runned

    def running_average(self, spectrum: numpy.ndarray) -> numpy.ndarray:
        runned = [1/4 * spectrum[i - 1] + 1/2 * spectrum[i] + 1/4 * spectrum[i + 1] for i in range(1, len(spectrum) - 1)]

        runned.insert(0, spectrum[0])
        runned.append(spectrum[-1])

        return numpy.array(runned)
    
    def residual_smooth(self, spectrum: numpy.ndarray, smoothed: numpy.ndarray) -> numpy.ndarray:
        rough = spectrum - smoothed

        rough = self.running_median(rough, 3)
        rough = self.running_median(rough, 5)
        rough = self.running_median(rough, 3)
        rough = self.running_average(rough)

        return rough
    
    def _median_of(self, seq: numpy.ndarray) -> int:
        return numpy.sort(seq, kind='mergesort')[len(seq) // 2]


if __name__ == '__main__':
    pass
