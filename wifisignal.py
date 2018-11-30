import subprocess
from coordinate import Coordinate2D


# User's perspective
# For receiving the wifi signal data(probably receives as JSON format)
class WifiSignalData:
    def __init__(self, ssid, bssid, rssi):
        self.ssid = ssid
        self.bssid = bssid
        self.rssi = rssi

    @property
    def ssid(self):
        return self.ssid

    @property
    def bssid(self):
        return self.bssid

    @property
    def rssi(self):
        return self.rssi

    def get_access_points(self):
        # cmd = "netsh wlan show networks mode=bssid" # all the APs I communicate with
        cmd = "netsh wlan show interfaces"  # the one I'm connected to
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (out, _) = proc.communicate()
        return out

    def move_cursor(self, target, cursor):
        return target[cursor:]

    def get_ssid(self, AP_result):
        pos = AP_result.find('SSID')
        if pos == -1:
            return None, -1

        AP_result = self.move_cursor(AP_result, pos)
        ap_ssid = AP_result.split('\n')[0].split(':')[-1].strip()

        return AP_result, ap_ssid

    def get_ap_bssid(self, AP_result):
        pos = AP_result.find('BSSID')
        AP_result = self.move_cursor(AP_result, pos)
        ap_bssid = AP_result.split('\n')[0].strip()[-17:]

        return AP_result, ap_bssid

    def get_ap_signal(self, AP_result):
        pos = AP_result.find('Signal')
        AP_result = self.move_cursor(AP_result, pos)
        ap_signal = AP_result.split('\n')[0].split(':')[-1].strip()
        AP_result = self.move_cursor(AP_result, pos + len(ap_signal))

        return AP_result, ap_signal
