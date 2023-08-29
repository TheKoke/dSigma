from __future__ import annotations
from business.physics import Nuclei


class Detector:
    def __init__(self, madeof: str, thickness: float, resolution: float = 0.01) -> None:
        self.__madeof = madeof
        self.__thickness = thickness
        self.__resolution = resolution

    @property
    def madeof(self) -> str:
        return self.__madeof
    
    @property
    def madeof_nuclei(self) -> Nuclei:
        match self.__madeof.lower():
            case 'ge': return Nuclei(32, 72)
            case 'si': return Nuclei(14, 28)
            case _: return Nuclei(14, 28)
    
    @property
    def thickness(self) -> float:
        return self.__thickness
    
    @property
    def resolution(self) -> float:
        return self.__resolution
    
    @property
    def density(self) -> float:
        match self.__madeof.lower():
            case 'ge': return 5.323
            case 'si': return 2.330
            case _: return 1.000

    def __eq__(self, other: Detector) -> bool:
        return self.madeof_nuclei == other.madeof_nuclei and \
               self.thickness == other.thickness and \
               self.resolution == other.resolution


class Telescope:
    def __init__(self, e_detector: Detector, de_detector: Detector, 
                 kollimator_radius: float = 1.0, distance: float = 360,
                 integrator_constant: float = 1e-10) -> None:
        self.__e_detector = e_detector
        self.__de_detector = de_detector
        
        self.__distance = distance
        self.__collimator_radius = kollimator_radius
        self.__integrator_constant = integrator_constant

    @property
    def e_detector(self) -> Detector:
        return self.__e_detector
    
    @property
    def de_detector(self) -> Detector:
        return self.__de_detector
    
    @property
    def collimator_radius(self) -> float:
        return self.__collimator_radius
    
    @property
    def distance(self) -> float:
        return self.__distance
    
    @property
    def integrator_constant(self) -> float:
        return self.__integrator_constant
    
    def __eq__(self, other: Telescope) -> bool:
        return self.e_detector == other.e_detector and \
        self.integrator_constant == other.integrator_constant
    

if __name__ == '__main__':
    pass
