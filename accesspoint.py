from coordinate import Coordinate2D


# For AP information data
class AccessPoint:

    def __init__(self, bssid, freq, pos, transmit_power=-999.0):
        self.ssid = ''
        self.bssid = bssid
        self.freq = freq
        self.pos = Coordinate2D(pos)  # type : tuple , content: (x,y) coord
        self.transmit_power = transmit_power

    """ getter & setter ------------------------------------------------------------------------ """

    @property
    def ssid(self):
        return self.ssid

    @property
    def bssid(self):
        return self.bssid

    @property
    def freq(self):
        return self.freq

    @property
    def pos(self):
        return self.pos

    @property
    def transmit_power(self):
        return self.transmit_power

    @ssid.setter
    def ssid(self, value):
        self.ssid = value

    @transmit_power.setter
    def transmit_power(self, value):
        self.transmit_power = value
