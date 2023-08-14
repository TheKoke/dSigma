from __future__ import annotations


Z_MINUS_N = (2, 3)
NEUTRON = (6, 8)
PROTON = (11, 13)
NUCLON = (16, 18)
NAME = (20, 21)
MASS_EXCESS = 28


def mass_excess_of(z: int, a: int) -> float:
    buffer = open('ame2020.txt', 'r').read().split('\n')[36:]

    start_area, stop_area = find_nuclons_index(buffer, a)
    neutrons = a - z

    for i in range(start_area, stop_area):
        if take_neutrons(buffer[i]) == neutrons:
            return take_mass_excess(buffer[i]) * 1e-3
        
    raise ValueError(f'Could not find nuclei with {z} protons and {a} nuclons.')

def find_nuclons_index(buffer: list[str], nuclons: int) -> tuple[int, int]:
    start, stop = 0, 0
    is_started = False

    for i in range(len(buffer)):
        if take_nuclons(buffer[i]) == nuclons and not is_started:
            start = i
            is_started = True

        if take_nuclons(buffer[i]) != nuclons and is_started:
            stop = i
            break

    return (start, stop)

def take_nuclons(line: str) -> int:
    return int(read_area(line, *NUCLON))

def take_charge(line: str) -> int:
    return int(read_area(line, *PROTON))

def take_neutrons(line: str) -> int:
    return int(read_area(line, *NEUTRON))

def take_mass_excess(line: str) -> int:
    seen = ''
    is_started = False

    for i in range(MASS_EXCESS, len(line)):
        if line[i] == ' ' and is_started:
            break

        is_symbol = line[i] == '-' or line[i] == '.'
        if line[i].isdigit() or is_symbol:
            is_started = len(seen) != 0
            seen += line[i]

    return float(seen)

def read_area(line: str, start: int, stop: int) -> float:
    seen = ''
    for i in range(start, stop + 1):
        is_symbol = line[i] == '-' or line[i] == '.'

        if line[i].isdigit() or is_symbol:
            seen += line[i]

    return float(seen)


if __name__ == '__main__':
    print(mass_excess_of(1, 2))
