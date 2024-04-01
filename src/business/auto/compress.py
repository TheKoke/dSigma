import numpy


def squash(data: numpy.ndarray, n: int) -> numpy.ndarray:
    if len(data) <= n:
        return numpy.array(data + [0] * (n - len(data)))
    
    cost = len(data) / n

    compressed = []
    for i in range(n):
        start = cost * i
        stop = cost * (i + 1) - 1

        start_ceil = int(numpy.ceil(start))
        start_floor = int(numpy.floor(start))
        
        stop_ceil = int(numpy.ceil(stop))
        stop_floor = int(numpy.ceil(stop))

        fully_covered = sum(data[start_ceil: stop_floor + 1])
        partially_covered = int(data[start_floor] * (start_ceil - start))
        partially_covered += int(data[stop_ceil] * (stop - stop_floor))

        compressed.append(fully_covered + partially_covered)

    return numpy.array(compressed)


if __name__ == '__main__':
    pass
