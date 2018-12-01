import subprocess
from coordinate import Coordinate2D


class Signal:
    def __init__(self, ssid='', bssid='', rssi=-999, group=''):
        self.ssid = ssid
        self.bssid = bssid
        self.rssi = rssi
        self.group = group

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
        self.signal_list = []
        self.strongest_signal_list = []
        self.anchor_signal = None

    @property
    def strongest_signal_list(self):
        return self.strongest_signal_list

    @property
    def signal_list(self):
        return self.signal_list

    @property
    def anchor_signal(self):  # the most strongest signal (highest RSSI)
        return self.anchor_signal

    # JSON, PARSING
    def receive_data(self):
        # for each data : loop
        #     self.signal_list.append(Signal(data['SSID'],data['BSSID'],data['RSSI']))
        pass

    # getting the 'num_of_groups' number of dominant signals
    def find_dominant_signal(self, num_of_groups):
        # initialize strongest_signal_list : !!!!!!!!!!!!!THIS ONE DOES NOT INCLUDE ANCHOR SIGNAL!!!!!!!!!!!!!
        self.strongest_signal_list.append(Signal('Wolfie', '7A:E0', -65, 'H1'))
        self.strongest_signal_list.append(Signal('Wolfie', '77:00', -50, 'H2'))

        # the most strongest signal
        self.anchor_signal = Signal('Wolfie', 'FC:80', -45, 'H3')
        pass
