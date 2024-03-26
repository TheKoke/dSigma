import numpy


class Density:
    def __init__(self, matrix: numpy.ndarray, averaging: bool = False, adding_up: bool = True, zero_encount_limit: int = 9) -> None:
        self._matrix = matrix
        self._density = numpy.array([], dtype=numpy.int32)

        if averaging ^ adding_up:
            averaging = False
            adding_up = True

        self._averaging = averaging
        self._adding_up = adding_up
        self._zero_encount = zero_encount_limit

    @property
    def density_matrix(self) -> numpy.ndarray:
        if len(self._density) == 0:
            self._calculate()
        
        return self._density.copy()

    def _calculate(self) -> None:
        self._density = self._matrix.copy()

        for i in range(len(self._matrix)):
            for j in range(len(self._matrix[i])):
                self._density[i, j] = self._point_density(i, j)

    def _point_density(self, i: int, j: int) -> int:
        neighrs = []

        for di in [-1, 0, 1]:
            if i + di < 0 or i + di >= len(self._matrix):
                continue

            for dj in [-1, 0, 1]:
                if j + dj < 0 or j + dj >= len(self._matrix[i + di]):
                    continue

                neighrs.append(self._matrix[i + di, j + dj])

        if neighrs.count(0) >= self._zero_encount:
            return 0
        
        if self._averaging:
            return sum(neighrs) // len(neighrs)
        
        if self._adding_up:
            return sum(neighrs)


if __name__ == '__main__':
    pass
