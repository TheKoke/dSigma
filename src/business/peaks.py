import numpy


class Gaussian:
    def __init__(self, mu: float, sigma: float, area: float) -> None:
        self.__mu = mu
        self.__dispersion = sigma
        self.__area = area

    @property
    def mu(self) -> float:
        return self.__mu
    
    @property
    def dispersion(self) -> float:
        return self.__dispersion
    
    @property
    def area(self) -> float:
        return self.__area
    
    @property
    def fwhm(self) -> float:
        return self.__dispersion * (2 * numpy.sqrt(2 * numpy.log(2)))
    
    def to_workbook(self) -> str:
        return f'Peak on mu=({round(self.mu, 3)}) with fwhm=({round(self.fwhm, 3)}) and area under peak=({round(self.area, 3)})'

    def __str__(self) -> str:
        func = 'G(x) = '
        func += f'{numpy.round(self.area, 3)} / (sqrt(2pi * {numpy.round(self.dispersion, 3)}) * '
        func += f'exp(-(x - {numpy.round(self.mu, 3)})^2 / 2{numpy.round(self.dispersion, 3)})'

        return func

    def three_sigma(self) -> numpy.ndarray:
        return numpy.linspace(-3 * self.__dispersion + self.__mu, 3 * self.__dispersion + self.__mu, 100)
    
    def function(self) -> numpy.ndarray:
        constant = self.__area / numpy.sqrt(2 * numpy.pi * numpy.power(self.__dispersion, 2))
        array = numpy.exp(-numpy.power(self.three_sigma() - self.__mu, 2) / (2 * numpy.power(self.__dispersion, 2)))
        return constant * array
    

class Lorentzian:
    def __init__(self, mu: float, fwhm: float, area: float) -> None:
        self.mu = mu
        self.fwhm = fwhm
        self.area = area

    def to_workbook(self) -> str:
        return f'Peak on mu=({round(self.mu, 3)}) with fwhm=({round(self.fwhm, 3)}) and area under peak=({round(self.area, 3)})'

    def __str__(self) -> str:
        func = 'L(x) = '
        func += f'2 * {round(self.area, 3)} / pi'
        func += f'* [{numpy.round(self.fwhm, 3)} / ((x - {round(self.mu)})^2 + {round(self.fwhm, 3)}^2)]'

        return func
    
    def dispersion(self) -> float:
        return self.fwhm / (2 * numpy.sqrt(2 * numpy.log(2)))
    
    def three_sigma(self) -> numpy.ndarray:
        sigma = self.dispersion()
        return numpy.linspace(-5 * sigma + self.mu, 5 * sigma + self.mu, 50)
    
    def function(self) -> numpy.ndarray:
        constant = 2 * self.area / numpy.pi
        brackets = self.fwhm / (4 * (self.three_sigma() - self.mu) ** 2 + self.fwhm ** 2)

        return constant * brackets


if __name__ == '__main__':
    pass
