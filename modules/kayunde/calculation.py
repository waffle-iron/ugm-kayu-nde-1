""" Nondestructive evaluation of wood calculation
"""

from math import pow as mathpow

class Kayu():
    """ Class for kayu - kayu is a term in Bahasa means wood
    Units:
            * All the units are in SI
            * kg, meter, kHz, MPa
    """

    def __init__(self, weight, length, thick_x, thick_y):
        self.weight = weight
        self.length = length
        self.thick_x = thick_x
        self.thick_y = thick_y
        self.volume = length * thick_x * thick_y
        self.density = weight / self.volume
        self.__freq = None
        self.__moe = None

    def set_freq(self, freq):
        """ Set the natural frequency of the wood
        """
        self.__freq = freq

    def get_freq(self):
        """ Get the natural frequency of the wood
		"""
        return self.__freq

    def get_moe(self):
        """ Get the MOE of the wood
		"""
        self.__moe = 4 * mathpow(self.__freq, 2) * mathpow(self.length, 2) * self.density #Formula of Dynamic MOE
        return self.__moe

class KayuPi(Kayu):
    """ The kayu class for recording via raspberry pi
    """
    def __init__(self, weight, length, thick_x, thick_y, duration):
        Kayu.__init__(self, weight, length, thick_x, thick_y)
        self.duration = duration
