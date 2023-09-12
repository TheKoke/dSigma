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
    
    @madeof.setter
    def madeof(self, val: str) -> None:
        if val.lower() not in ['ge', 'si', 'c3h6']:
            return
        self.__madeof = val
    
    @property
    def madeof_nuclei(self) -> Nuclei:
        match self.__madeof.lower():
            case 'ge': return Nuclei(32, 72)
            case 'si': return Nuclei(14, 28)
            case _: return Nuclei(14, 28)
    
    @property
    def thickness(self) -> float:
        return self.__thickness
    
    @thickness.setter
    def thickness(self, val: float) -> None:
        if val <= 0:
            return
        self.__thickness = val
    
    @property
    def resolution(self) -> float:
        return self.__resolution
    
    @resolution.setter
    def resolution(self, val: float) -> None:
        if val < 0:
            return
        self.__resolution = val
    
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
                 kollimator_radius: float = 1.0, distance: float = 360) -> None:
        self.__e_detector = e_detector
        self.__de_detector = de_detector
        
        self.__distance = distance
        self.__collimator_radius = kollimator_radius

    @property
    def e_detector(self) -> Detector:
        return self.__e_detector
    
    @property
    def de_detector(self) -> Detector:
        return self.__de_detector
    
    @property
    def collimator_radius(self) -> float:
        return self.__collimator_radius
    
    @collimator_radius.setter
    def collimator_radius(self, val: float) -> None:
        if val >= 0:
            return
        self.__collimator_radius = val
    
    @property
    def distance(self) -> float:
        return self.__distance
    
    @distance.setter
    def distance(self, val: float) -> None:
        if val <= 0:
            return
        self.__distance = val
    
    def __eq__(self, other: Telescope) -> bool:
        return self.e_detector == other.e_detector
    

if __name__ == '__main__':
    pass
