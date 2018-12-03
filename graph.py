import matplotlib.pyplot as plt
import numpy as np
from accesspoint import AccessPoint


# SB
class SignalBin:
    def __init__(self, group):
        self.group = group
        self.rssi_2_4GHz_sum = 0  # accumulate it inside one iteration, empty it when iteration ends
        self.rssi_5_0GHz_sum = 0
        self.count_2_4GHz_sum = 0
        self.count_5_0GHz_sum = 0

        self.final_2_4GHz = []  # final 2.4GHz bin
        self.final_5_0GHz = []  # final 5.0GHz bin

        self.lowest_value = -70.0

    @property
    def rssi_2_4GHz_sum(self):
        return self.rssi_2_4GHz_sum

    @property
    def rssi_5_0GHz_sum(self):
        return self.rssi_5_0GHz_sum

    @property
    def count_2_4GHz_sum(self):
        return self.count_2_4GHz_sum

    @property
    def count_5_0GHz_sum(self):
        return self.count_5_0GHz_sum

    @property
    def final_2_4GHz(self):
        return self.final_2_4GHz

    @property
    def final_5_0GHz(self):
        return self.final_5_0GHz

    @rssi_2_4GHz_sum.setter
    def rssi_2_4GHz_sum(self, value):
        self.rssi_2_4GHz_sum = value

    @rssi_5_0GHz_sum.setter
    def rssi_5_0GHz_sum(self, value):
        self.rssi_5_0GHz_sum = value

    @count_2_4GHz_sum.setter
    def count_2_4GHz_sum(self, value):
        self.count_2_4GHz_sum = value

    @count_5_0GHz_sum.setter
    def count_5_0GHz_sum(self, value):
        self.count_5_0GHz_sum = value

    def set_final_2_4GHz(self, value):
        self.final_2_4GHz.append(value)

    def set_final_5_0GHz(self, value):
        self.final_5_0GHz.append(value)

    # accumulate it inside one iteration, empty it when iteration ends
    def initialze_all(self):
        self.rssi_2_4GHz_sum = 0
        self.rssi_5_0GHz_sum = 0
        self.count_2_4GHz_sum = 0
        self.count_5_0GHz_sum = 0

    def get_avg_2_4GHz(self):
        if self.count_2_4GHz_sum == 0:
            return self.lowest_value
        else:
            return float(self.rssi_2_4GHz_sum) / self.count_2_4GHz_sum

    def get_avg_5_0GHz(self):
        if self.count_5_0GHz_sum == 0:
            return self.lowest_value
        else:
            return float(self.rssi_5_0GHz_sum) / self.count_5_0GHz_sum


def get_freq(ap_list, target_bssid):
    freq = -1
    for data in ap_list:
        if target_bssid.endswith(data.bssid):
            freq = data.freq
            break

    return freq


def init_sum_SB(dict):
    for key in dict.keys():
        dict[key].initialze_all()


def save_avg_signal_SB(dict):
    for key in dict.keys():
        SB_instance = dict[key]
        avg_2_4 = SB_instance.get_avg_2_4GHz()
        avg_5_0 = SB_instance.get_avg_5_0GHz()
        SB_instance.set_final_2_4GHz(avg_2_4)
        SB_instance.set_final_5_0GHz(avg_5_0)


def draw_graph(signal_bin_dict, num_of_iter):
    # the graph should look like this:
    # Graph 1) 2.4GHz
    # x-axis : physical location (e.g. from H4 H3 H2 H1 L2 L1 )
    # y-axis : RSSI : 10 graphs' lines with diff. colors (representing 2.4GHz)

    # Graph 2) 5.0GHz
    # x-axis : physical location
    # y-axis : RSSI : 10 graphs' lines with diff. colors (representing 5.0GHz)

    # : -30 meter ~ 32 meter (from the point of origin : H2)
    # measure every 1 meter starting from NCS's very-end-wall (H4-side)
    # x = range(-30, 33) # this is REQUIRED
    x = np.linspace(-1, 1, num_of_iter + 1)  # THIS IS ONLY FOR TESTING

    # !!!!!!!!!!!!!!!!!!!!!!!!!!THE NUMBER OF MEASURED DATA SHOULD BE 63 (= 63 ITERATION)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!THE NUMBER OF MEASURED DATA SHOULD BE 63 (= 63 ITERATION)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!THE NUMBER OF MEASURED DATA SHOULD BE 63 (= 63 ITERATION)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!THE NUMBER OF MEASURED DATA SHOULD BE 63 (= 63 ITERATION)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!THE NUMBER OF MEASURED DATA SHOULD BE 63 (= 63 ITERATION)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Graph 1) 2.4GHz
    for signal_key in signal_bin_dict.keys():
        y1 = None
        y1 = signal_bin_dict[signal_key].final_2_4GHz
        plt.plot(x, y1, label=signal_key, linewidth=0.75, linestyle=':', color='gray')

    # # Graph 2) 5.0GHz
    # for signal_key in signal_bin_dict.keys():
    #     y2 = None
    #     y2 = signal_bin_dict[signal_key].final_5_0GHz
    #     plt.plot(x, y2, label=signal_key)

    plt.xlabel('Distance')
    plt.ylabel('RSSI')
    plt.title('Signal pattern\n')

    # plt.legend()
    plt.show()


if __name__ == "__main__":
    AP_list = {'H1': [AccessPoint('7A:E0', 2.4, (0.0, 9.1440), -1), AccessPoint('7A:E1', 2.4, (0.0, 9.1440), -1),
                      AccessPoint('7A:E3', 2.4, (0.0, 9.1440), -1), AccessPoint('7A:F0', 5.0, (0.0, 9.1440), -1),
                      AccessPoint('7A:F1', 5.0, (0.0, 9.1440), -1), AccessPoint('7A:F3', 5.0, (0.0, 9.1440), -1)],

               'H2': [AccessPoint('77:00', 2.4, (0.0, 0.0), -1), AccessPoint('77:01', 2.4, (0.0, 0.0), -1),
                      AccessPoint('77:03', 2.4, (0.0, 0.0), -1), AccessPoint('77:10', 5.0, (0.0, 0.0), -1),
                      AccessPoint('77:11', 5.0, (0.0, 0.0), -1), AccessPoint('77:13', 5.0, (0.0, 0.0), -1)],

               'H3': [AccessPoint('FC:80', 2.4, (0.0, -14.6050), -1), AccessPoint('FC:82', 2.4, (0.0, -14.6050), -1),
                      AccessPoint('FC:83', 2.4, (0.0, -14.6050), -1), AccessPoint('FC:90', 5.0, (0.0, -14.6050), -1),
                      AccessPoint('FC:92', 5.0, (0.0, -14.6050), -1), AccessPoint('FC:93', 5.0, (0.0, -14.6050), -1)],

               'H4': [AccessPoint('77:60', 2.4, (0.0, -27.4320), -1), AccessPoint('77:61', 2.4, (0.0, -27.4320), -1),
                      AccessPoint('77:63', 2.4, (0.0, -27.4320), -1), AccessPoint('77:70', 5.0, (0.0, -27.4320), -1),
                      AccessPoint('77:71', 5.0, (0.0, -27.4320), -1), AccessPoint('77:73', 5.0, (0.0, -27.4320), -1)],

               'P1': [AccessPoint('7A:C0', 2.4, (21.4884, 21.6662), -1),
                      AccessPoint('7A:C1', 2.4, (21.4884, 21.6662), -1),
                      AccessPoint('7A:C3', 2.4, (21.4884, 21.6662), -1),
                      AccessPoint('7A:D0', 5.0, (21.4884, 21.6662), -1),
                      AccessPoint('7A:D1', 5.0, (21.4884, 21.6662), -1),
                      AccessPoint('7A:D3', 5.0, (21.4884, 21.6662), -1)],

               'P2': [AccessPoint('7B:A0', 2.4, (10.5410, 21.6662), -1),
                      AccessPoint('7B:A1', 2.4, (10.5410, 21.6662), -1),
                      AccessPoint('7B:A3', 2.4, (10.5410, 21.6662), -1),
                      AccessPoint('7B:B0', 5.0, (10.5410, 21.6662), -1),
                      AccessPoint('7B:B1', 5.0, (10.5410, 21.6662), -1),
                      AccessPoint('7B:B3', 5.0, (10.5410, 21.6662), -1)],

               'L1': [AccessPoint('85:E0', 2.4, (0.0, 31.5976), -1), AccessPoint('85:E2', 2.4, (0.0, 31.5976), -1),
                      AccessPoint('85:E3', 2.4, (0.0, 31.5976), -1), AccessPoint('85:F0', 5.0, (0.0, 31.5976), -1),
                      AccessPoint('85:F2', 5.0, (0.0, 31.5976), -1), AccessPoint('85:F3', 5.0, (0.0, 31.5976), -1)],

               'L2': [AccessPoint('7C:00', 2.4, (0.0, 17.0434), -1), AccessPoint('7C:01', 2.4, (0.0, 17.0434), -1),
                      AccessPoint('7C:03', 2.4, (0.0, 17.0434), -1), AccessPoint('7C:10', 5.0, (0.0, 17.0434), -1),
                      AccessPoint('7C:11', 5.0, (0.0, 17.0434), -1), AccessPoint('7C:13', 5.0, (0.0, 17.0434), -1)],

               # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
               # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
               # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
               # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
               # CHECK THE MAC ADDRESS FOR S1 AND S2# CHECK THE MAC ADDRESS FOR S1 AND S2
               # CHECK THE MAC ADDRESS FOR S1 AND S2# CHECK THE MAC ADDRESS FOR S1 AND S2

               'S2': [AccessPoint('85:A0', 2.4, (-5.6896, 21.6281), -1),
                      AccessPoint('85:A1', 2.4, (-5.6896, 21.6281), -1),
                      AccessPoint('85:A3', 2.4, (-5.6896, 21.6281), -1),
                      AccessPoint('85:B0', 5.0, (-5.6896, 21.6281), -1),
                      AccessPoint('85:B1', 5.0, (-5.6896, 21.6281), -1),
                      AccessPoint('85:B3', 5.0, (-5.6896, 21.6281), -1)],

               'S1': [AccessPoint('E1:60', 2.4, (-10.8966, 27.7241), -1),
                      AccessPoint('E1:62', 2.4, (-10.8966, 27.7241), -1),
                      AccessPoint('E1:63', 2.4, (-10.8966, 27.7241), -1),
                      AccessPoint('E1:70', 5.0, (-10.8966, 27.7241), -1),
                      AccessPoint('E1:72', 5.0, (-10.8966, 27.7241), -1),
                      AccessPoint('E1:73', 5.0, (-10.8966, 27.7241), -1)]}
    directory = './Record/'
    file_name = 'Record(181202_205925)' + '.txt'  # target file_name
    file_dir = directory + file_name
    signal_bin_dict = {
        'H1': SignalBin('H1'),
        'H2': SignalBin('H2'),
        'H3': SignalBin('H3'),
        'H4': SignalBin('H4'),
        'L1': SignalBin('L1'),
        'L2': SignalBin('L2'),
        'P1': SignalBin('P1'),
        'P2': SignalBin('P2'),
        'S1': SignalBin('S1'),
        'S2': SignalBin('S2')
    }
    is_data = False
    num_of_iter = 0
    with open(file_dir, 'r') as fp:
        for raw_data in fp:  # read data line by line
            if raw_data.startswith('-----'):
                is_data = True
                num_of_iter = num_of_iter + 1
                save_avg_signal_SB(signal_bin_dict)  # average each frequency signal
                init_sum_SB(signal_bin_dict)  # empty values
                continue
            elif raw_data == 'FINISH':
                save_avg_signal_SB(signal_bin_dict)  # average each frequency signal
                init_sum_SB(signal_bin_dict)  # empty values
                continue
            if is_data:
                data = raw_data[:-1]  # remove newline character
                splitted_data = data.split(' ')
                rssi = int(splitted_data[0])
                group = splitted_data[1]
                bssid = splitted_data[2]
                freq = get_freq(AP_list[group], bssid)

                # separately save 5.0GHz and 2.4GHz (2.4GHz signal travels too far: inaccurate for short range)
                if freq == 2.4:
                    signal_bin_dict[group].rssi_2_4GHz_sum = signal_bin_dict[group].rssi_2_4GHz_sum + rssi
                    signal_bin_dict[group].count_2_4GHz_sum = signal_bin_dict[group].count_2_4GHz_sum + 1
                elif freq == 5.0:
                    signal_bin_dict[group].rssi_5_0GHz_sum = signal_bin_dict[group].rssi_5_0GHz_sum + rssi
                    signal_bin_dict[group].count_5_0GHz_sum = signal_bin_dict[group].count_5_0GHz_sum + 1

    draw_graph(signal_bin_dict, num_of_iter)
