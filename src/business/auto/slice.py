import numpy


class Slicer:
    def __init__(self) -> None:
        pass

    def laddering(self, matrix: numpy.ndarray, step: int = 5) -> numpy.ndarray:
        parts = self.shred(matrix, step)

        mean = parts.mean()
        for i in range(len(parts)):
            parts[i] = parts[i] + i * mean * mean

        return parts
    
    def shred(self, matrix: numpy.ndarray, step: int = 5) -> dict[int, numpy.ndarray]:
        return {i : self.slice_at(matrix, i, step) for i in range(1, len(matrix), step)}

    def slice_at(self, matrix: numpy.ndarray, n: int, step: int = 5) -> numpy.ndarray:
        return matrix[:, n - step // 2 : n + step // 2].sum(axis=1)


if __name__ == '__main__':
    pass