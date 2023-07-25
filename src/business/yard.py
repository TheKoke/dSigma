from enum import Enum

from business.physics import Reaction, Nuclei


class ReactionNotation(Enum):
    SOVETIAN = 1
    CHEMIST = 2
    UNDEFINED = 3


class NucleiConverter:
    NAMES = {
        1:   'H', 2:  'He', 3:  'Li', 4:  'Be', 5:   'B', 6:   'C',
        7:   'N', 8:   'O', 9:   'F', 10: 'Ne', 11: 'Na', 12: 'Mg',
        13: 'Al', 14: 'Si', 15:  'P', 16:  'S', 17: 'Cl', 18: 'Ar',
        19:  'K', 10: 'Ca', 11: 'Sc', 22: 'Ti', 23:  'V', 24: 'Cr',
        25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zr',
        31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr' 
    }


    @staticmethod
    def to_string(nuclei: Nuclei) -> str:
        if nuclei.charge == 1:
            isotopes = ['p', 'd', 't']
            return isotopes[nuclei.nuclons - 1]

        return f'{nuclei.nuclons}{NucleiConverter.NAMES[nuclei.charge]}'

    @staticmethod
    def to_nuclei(input: str) -> Nuclei:
        input = input.strip()
        charge = NucleiConverter.charge_by_name(input)
        nuclons = NucleiConverter.nuclons_by_name(input)

        if charge == -1 or nuclons <= 0:
            raise ValueError('Input string was not nuclei.')
        
        if charge > nuclons:
            raise ValueError('Protons in nuclei cannot be more than all nuclons.')

        return Nuclei(charge, nuclons)

    @staticmethod
    def nuclons_by_name(name: str) -> int:
        name = name.lower()
        if name in ['p', 'd', 't']:
            return ['p', 'd', 't'].index(name) + 1
        elif name == 'a':
            return 4

        pretend = ''
        for i in name:
            if i.isdigit():
                pretend += i

        return int(pretend)

    @staticmethod
    def charge_by_name(name: str) -> int:
        name = ''.join([char.lower() for char in name if char.isalpha()])
        match name:
            case 'h' | 'p' | 'd' | 't': return 1
            case 'he' | 'a': return 2
            case 'li': return 3
            case 'be': return 4
            case 'b': return 5
            case 'c': return 6
            case 'n': return 7
            case 'o': return 8
            case 'f': return 9
            case _: return -1


class ReactionMaster:
    def __init__(self, input: str, energy: float) -> None:
        '''
        Nuclear reactions can wroted in 2 different styles:
        A(B, C)D - sovetian variant.
        A + B -> C + D - chemistry variant.
        '''
        self.reaction = input
        self.energy = energy

        self.notation = self.__define_notation()

    def __define_notation(self) -> ReactionNotation:
        if '(' in self.reaction and ')' in self.reaction:
            return ReactionNotation.SOVETIAN
        
        if '->' in self.reaction:
            return ReactionNotation.CHEMIST
        
        return ReactionNotation.UNDEFINED

    def to_reaction(self) -> Reaction:
        nucleus = self.split_nucleus()

        beam = self.to_nuclei(nucleus[0])
        target = self.to_nuclei(nucleus[1])
        fragment = self.to_nuclei(nucleus[2])

        return Reaction(beam, target, fragment, self.energy)

    def to_nuclei(self, name: str) -> Nuclei:
        nuclons = NucleiConverter.nuclons_by_name(name)
        charge = NucleiConverter.charge_by_name(name)
        return Nuclei(nuclons, charge)

    def split_nucleus(self) -> list[str]:
        no_spaces = self.reaction.replace(' ', '')

        if self.notation == ReactionNotation.UNDEFINED:
            raise ValueError('Reaction was written incorrectly.')

        if self.notation == ReactionNotation.SOVETIAN:
            return ReactionMaster.split_sovetian(no_spaces)

        if self.notation == ReactionNotation.CHEMIST:
            return ReactionMaster.split_chemistry(no_spaces)
    
    @staticmethod
    def split_sovetian(input: str) -> list[str]:
        halfs = input.split(',')

        first_half = halfs[0].split('(')
        second_half = halfs[1].split(')')

        beam, target = first_half[1], first_half[0]
        fragment, residual = second_half[0], second_half[1]

        return [beam, target, fragment, residual]
    
    @staticmethod
    def split_chemistry(input: str) -> list[str]:
        halfs = input.split('->')

        first_half = halfs[0].split('+')
        second_half = halfs[1].split('+')

        beam, target = first_half[1], first_half[0]
        fragment, residual = second_half[1], second_half[0]

        return [beam, target, fragment, residual]


if __name__ == '__main__':
    pass