import subprocess
from coordinate import Coordinate2D
import json


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
# For receiving the wifi signal data (receives as JSON format)
class WifiSignalParse:
    def __init__(self):
        self.signal_list = []
        self.target_signal_list = []
        self.anchor_signal = None

    @property
    def target_signal_list(self):
        return self.target_signal_list

    @property
    def signal_list(self):
        return self.signal_list

    @property
    def anchor_signal(self):  # the most strongest signal (highest RSSI)
        return self.anchor_signal

    # RECEIVING DATA FROM THE CLIENT as JSON format, and form it into my format
    def receive_data(self):
        # this part is for testing ------
        self.signal_list.append(Signal('Wolfie', 'FC:83', -42, 'H3'))
        self.signal_list.append(Signal('Wolfie', 'FC:93', -42, 'H3'))
        self.signal_list.append(Signal('Wolfie', 'FC:90', -42, 'H3'))
        self.signal_list.append(Signal('Wolfie', 'FC:92', -42, 'H3'))
        self.signal_list.append(Signal('Wolfie', 'FC:82', -46, 'H3'))

        self.signal_list.append(Signal('Wolfie', '77:63', -49, 'H4'))
        self.signal_list.append(Signal('Wolfie', '77:73', -53, 'H4'))
        self.signal_list.append(Signal('Wolfie', '77:70', -53, 'H4'))
        self.signal_list.append(Signal('Wolfie', 'FC:80', -55, 'H3'))
        self.signal_list.append(Signal('Wolfie', '77:61', -55, 'H4'))
        self.signal_list.append(Signal('Wolfie', '7A:F3', -55, 'H1'))

        self.signal_list.append(Signal('Wolfie', '77:13', -56, 'H2'))
        self.signal_list.append(Signal('Wolfie', '77:11', -56, 'H2'))
        self.signal_list.append(Signal('Wolfie', '7A:F1', -56, 'H1'))
        self.signal_list.append(Signal('Wolfie', '7C:13', -57, 'L2'))
        self.signal_list.append(Signal('Wolfie', '7A:F0', -57, 'H1'))

        self.signal_list.append(Signal('Wolfie', '77:71', -59, 'H4'))
        self.signal_list.append(Signal('Wolfie', '77:03', -61, 'H2'))
        self.signal_list.append(Signal('Wolfie', '77:00', -62, 'H2'))

        self.signal_list.append(Signal('Wolfie', '7A:E1', -63, 'H1'))
        self.signal_list.append(Signal('Wolfie', '77:60', -64, 'H4'))
        self.signal_list.append(Signal('Wolfie', '7A:E0', -64, 'H1'))
        self.signal_list.append(Signal('Wolfie', '7A:E3', -64, 'H1'))



        # -------------------------------

        # anchor_signal is the most the most strongest signal among received data
        # the most strongest signal is the first element of the received data (already sorted from client-side)
        self.anchor_signal = self.signal_list[0]

        # the list wihtout the anchor signal (the first signal)
        self.target_signal_list = self.signal_list[1:]

        # for each data : loop (for each wifi signal)
        #     json.loads(last_json)) # CORRECT GRAMMAR ??
        #     self.signal_list.append(Signal(data['SSID'],data['BSSID'],data['RSSI'], data['GROUP']))
        pass

    def find_dominant_signal(self, num_of_groups=-1):
        if num_of_groups == -1:  # use all the wifi signals (not only few('num_of_groups') of them)
            pass
        else:  # getting the 'num_of_groups' number of dominant signals
            pass
        pass
