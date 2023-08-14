from business.ameparse import mass_excess_of
from business.ensdf import excitation_energies, gammas


CHARGE2NAME = {
    0  :  'n',
    1  :  'H', 2  : 'He', 3  : 'Li', 4  : 'Be', 5  :  'B', 6  :  'C',
    7  :  'N', 8  :  'O', 9  :  'F', 10 : 'Ne', 11 : 'Na', 12 : 'Mg',
    13 : 'Al', 14 : 'Si', 15 :  'P', 16 :  'S', 17 : 'Cl', 18 : 'Ar',
    19 :  'K', 20 : 'Ca', 21 : 'Sc', 22 : 'Ti', 23 :  'V', 24 : 'Cr',
    25 : 'Mn', 26 : 'Fe', 27 : 'Co', 28 : 'Ni', 29 : 'Cu', 30 : 'Zr',
    31 : 'Ga', 32 : 'Ge', 33 : 'As', 34 : 'Se', 35 : 'Br', 36 : 'Kr',
    37 : 'Rb', 38 : 'Sr', 39 :  'Y', 40 : 'Zr', 41 : 'Nb', 42 : 'Mo',
    43 : 'Tc', 44 : 'Ru', 45 : 'Rh', 46 : 'Pd', 47 : 'Ag', 48 : 'Cd',
    49 : 'In', 50 : 'Sn', 51 : 'Sb', 52 : 'Te', 53 :  'I', 54 : 'Xe',
    55 : 'Cs', 56 : 'Ba', 57 : 'La', 58 : 'Ce', 59 : 'Pr', 60 : 'Nd',
    61 : 'Pm', 62 : 'Sm', 63 : 'Eu', 64 : 'Gd', 65 : 'Tb', 66 : 'Dy',
    67 : 'Ho', 68 : 'Er', 69 : 'Tm', 70 : 'Yb', 71 : 'Lu', 72 : 'Hf',
    73 : 'Ta', 74 :  'W', 75 : 'Re', 76 : 'Os', 77 : 'Ir', 78 : 'Pt',
    79 : 'Au', 80 : 'Hg', 81 : 'Tl', 82 : 'Pb', 83 : 'Bi', 84 : 'Po',
    85 : 'At', 86 : 'Rn', 87 : 'Fr', 88 : 'Ra', 89 : 'Ac', 90 : 'Th',
    91 : 'Pa', 92 :  'U', 93 : 'Np', 94 : 'Pu', 95 : 'Am', 96 : 'Cm',
    97 : 'Bk', 98 : 'Cf', 99 : 'Es', 100: 'Fm', 101: 'Md', 102: 'No',
    103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh', 108: 'Hs',
    109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn', 113: 'Nh', 114: 'Fl',
    115: 'Mc', 116: 'Lv', 117: 'Ts', 118: 'Og'
}


class Informator:

    @staticmethod
    def all_information(z: int, a: int) -> list:
        '''
        Method for take all database information for nuclei.\n
        Returns list of elements in this order:\n
        [mass excess, states, wigner widths]
        '''
        massexcess = Informator.mass_excess(z, a)
        states = Informator.states(z, a)
        widths = Informator.wigner_widths(z, a)

        return [massexcess, states, widths]
    
    @staticmethod
    def name(z: int, a: int) -> str:
        if z == 0 and a == 1:
            return 'n'
        
        if z == 1:
            isotopes = ['p', 'd', 't']
            return isotopes[a - 1]

        return f'{a}{CHARGE2NAME[z]}'

    @staticmethod
    def mass_excess(z: int, a: int) -> float:
        return mass_excess_of(z, a)

    @staticmethod
    def states(z: int, a: int) -> list[float]:
        return excitation_energies(z, a)

    @staticmethod
    def wigner_widths(z: int, a: int) -> list[float]:
        return gammas(z, a)


if __name__ == '__main__':
    pass
