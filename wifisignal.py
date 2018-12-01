import subprocess
from coordinate import Coordinate2D


class Signal:
    def __init__(self, ssid='', bssid='', rssi=-999):
        self.ssid = ssid
        self.bssid = bssid
        self.rssi = rssi
        self.group = ''

    @property
    def ssid(self):
        return self.ssid

    @property
    def bssid(self):
        return self.bssid

    @property
    def rssi(self):
        return self.rssi

    @property
    def group(self):
        return self.group


# User's perspective
# For receiving the wifi signal data(probably receives as JSON format)
class WifiSignalParse:
    def __init__(self):
        self.test = Signal()
        self.signal_list = []
        self.strongest_signal_list = []

    @property
    def strongest_signal_list(self):
        return self.strongest_signal_list

    @property
    def signal_list(self):
        return self.signal_list

    # JSON, PARSING
    def receive_data(self):
        # for each data : loop
        #     self.signal_list.append(Signal(data['SSID'],data['BSSID'],data['RSSI']))
        pass

    # getting the 'num_of_groups' number of dominant signals
    def find_dominant_signal(self, num_of_groups):
        # initialize strongest_signal_list
        pass
