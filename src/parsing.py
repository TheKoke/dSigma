import numpy as np

class USBParser:
    def __init__(self, path: str, size: int) -> None:
        self.path = path
        self.size = size
        self.binary_sizes = (0, 256 ** 2, 4)

    def set_binary(self, start: int, stop: int, step: int) -> None:
        self.binary_sizes = (start, stop, step)

    def generate_matrix(self) -> np.ndarray:
        source = open(self.path, 'rb').read()
        events = np.array([], dtype=np.uint32)

        for i in range(self.binary_sizes[0], self.binary_sizes[1], self.binary_sizes[2]):
            events = np.append(events, int(source[i]))

        return events.reshape(self.size, self.size)

    def generate_file(self, extension: str) -> str:
        array = self.generate_matrix()

        final = open(self.__generate_path(extension), 'w')
        for i in range(len(array)):
            for j in range(len(array)):
                final.write(str(array[i, j]) + ', ')
            final.write('\n')

        final.close()
        return self.__generate_path(extension)

    def __generate_path(self, extension: str) -> str:
        folder = '\\'.join(self.path.split('\\')[:-1])
        name = ''.join(self.path.split('\\')[-1].split('.')[:-1])

        return folder + '\\' + name + '.' + extension