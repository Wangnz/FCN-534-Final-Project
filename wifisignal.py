import subprocess
import json
from coordinate import Coordinate2D
from readData import get_access_points


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
    def receive_data(self, ap_map):
        ap_list = get_access_points()
        grouped = {}
        for ap in ap_list:
            if ap['GROUP'] not in grouped:
                grouped[ap['GROUP']] = []

            grouped[ap['GROUP']].append(Signal(ssid=ap['SSID'], bssid=ap['BSSID'], rssi=ap['RSSI'], group=ap['GROUP']))

        for group, ap_group in grouped.iteritems():
            rssi_sum = 0
            for signal in ap_group:
                rssi_sum += signal.rssi

            self.signal_list.append(
                Signal(ssid=signal, bssid=signal.bssid, rssi=rssi_sum / len(ap_group), group=signal.group))

        self.signal_list = sorted(self.signal_list, key=lambda e: e.rssi, reverse=True)
        print "signals", self.signal_list
        # anchor_signal is the strongest signal among received data
        # the strongest signal is the first element of the received data (already sorted from client-side)
        if len(self.signal_list) > 0:
            self.anchor_signal = self.signal_list[0]

        # the list wihtout the anchor signal (the first signal)
        if len(self.signal_list) > 1:
            self.target_signal_list = self.signal_list[1:]
            self.target_signal_list = self.signal_list[1:]

    def receive_data_test(self):
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

        self.anchor_signal = self.signal_list[0]
        self.target_signal_list = self.signal_list[1:]
