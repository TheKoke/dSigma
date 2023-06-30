class Detector:
    def __init__(self, madeof: str, thickness: float) -> None:
        self.__madeof = madeof
        self.__thickness = thickness

    @property
    def madeof(self) -> str:
        return self.__madeof
    
    @property
    def thickness(self) -> float:
        return self.__thickness
    
    def define_density(self) -> float:
        match self.__madeof.lower():
            case 'ge': return 5.323
            case 'si': return 2.330
            case _: return 1.000


class Telescope:
    def __init__(self, e_detector: Detector, de_detector: Detector, e_binning: int = 256, de_binning: int = 256) -> None:
        self.__e_detector = e_detector
        self.__de_detector = de_detector

        self.__e_binning = e_binning
        self.__de_binning = de_binning

    @property
    def e_detector(self) -> Detector:
        return self.__e_detector
    
    @property
    def de_detector(self) -> Detector:
        return self.__de_detector
    
    @property
    def e_binning(self) -> int:
        return self.__e_binning
    
    @property
    def de_binning(self) -> int:
        return self.__de_binning
    

if __name__ == '__main__':
    pass
