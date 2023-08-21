from business.ensdf import NAME2CHARGE, CHARGE2NAME
from business.ensdf import mass_excess_of, excitation_energies, gammas


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
