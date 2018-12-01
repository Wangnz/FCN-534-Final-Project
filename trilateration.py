import numpy as np
import time
import math
from accesspoint import AccessPoint
from wifisignal import WifiSignalParse


# --------------------------------------------------------------------------------------------------------------------

class Trilateration:

    def __init__(self):
        pass

    def get_estimated_distance(self, transmit_power, rssi):
        k = -27.55
        freq = 5200.0  # doesn't matter as long as it is consistent to get_transmit_power()'s frequency value
        dist = 10 ** ((transmit_power - rssi - k - 20.0 * math.log10(freq)) / 20.0)

        return dist

    # param: type=list, each element type=dict, content=[dist, x coord, y coord]
    def intersection_matrix(self, ap_list):
        ap_matrix_list_A = []
        ap_matrix_list_B = []
        ap_cnt = len(ap_list)

        # Xn's AP
        Xn = ap_list[ap_cnt - 1]['x']
        Yn = ap_list[ap_cnt - 1]['y']
        Rn = ap_list[ap_cnt - 1]['dist']  # radius
        # print Xn, Yn, Rn
        for i in xrange(ap_cnt - 1):  # for(i: 1 ~ n-1): Xi - Xn (e.g. X1-Xn , X2-Xn)
            Xi = ap_list[i]['x']
            Yi = ap_list[i]['y']
            Ri = ap_list[i]['dist']  # radius

            # AX = B : (x1^2 - xn^2 -2(x1-xn)x +y1^2 -yn^2 -2(y1-yn)y = r1^2 - rn^2
            A = 2 * np.array([Xi - Xn, Yi - Yn])
            B = np.array([(Xi ** 2) - (Xn ** 2) + (Yi ** 2) - (Yn ** 2) - (Ri ** 2) + (Rn ** 2)])
            ap_matrix_list_A.append(A)
            ap_matrix_list_B.append(B)

        matrix_A = np.reshape(ap_matrix_list_A, (-1, 2)).astype(np.float32)
        matrix_B = np.reshape(ap_matrix_list_B, (-1, 1)).astype(np.float32)
        return matrix_A, matrix_B

    # Get the centroid of all the circles
    def trilaterate(self, matrix_list_A, matrix_list_B):
        # Non-linear least square : X = [(A^t * A)^-1]*[A^t * B]
        # However!! we can just calculate the distance from each center of circles
        # setting the estimating position as (x,y),
        # and get the most equal(=fair or least square) distance from each circle's center points
        A = matrix_list_A
        B = matrix_list_B

        At = np.transpose(A)
        tmp = np.matmul(At, A)
        res1 = np.linalg.inv(tmp)
        res2 = np.matmul(At, B)

        estimated_position = np.matmul(res1, res2)

        return estimated_position

    # Get the user's current location
    def get_position(self, ap_list):
        matrix_A, matrix_B = self.intersection_matrix(ap_list)
        estimated_position_x, estimated_position_y = self.trilaterate(matrix_A, matrix_B).ravel()

        return estimated_position_x, estimated_position_y


def estimate_transmit_power():
    # # Initial number (dorm room)
    # dist = 2.1844  # reference value: in meters
    # rssi = -42.9  # reference value: in dBm
    # k = -27.55  # constant 'K' when using meters & MHz
    # freq = 5200.0  # in MHz (5G)

    # NCS Building
    dist = 2.8448
    rssi = -44.666667
    k = -27.55  # constant 'K' when using meters & MHz
    freq = 5200.0

    # Free Space Path Loss (FSPL) : the loss assuming that there are no obstacles btw receiver & transmitter
    # derived from FSPL = 20log(d) + 20log(f) - 27.55
    # Radio frequency transmission -> [Path loss(here using FSPL) = Pt(transmit_power) + G_total(0) - R(rssi)]
    transmit_power = 20.0 * math.log10(dist) + 20.0 * math.log10(freq) + rssi + k

    return transmit_power


def get_pos_with_group(ap_list, target_group, target_bssid):
    res = -1
    for ap in ap_list.keys():
        if ap == target_group:
            for data in ap_list[ap]:
                if data.bssid == target_bssid:
                    res = data.pos
                    break
        if res != -1:
            break
    return res


# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!
# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!
# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!
# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!
if __name__ == "__main__":
    # Initializing ------------------------------------------------------------------------------------------

    # CHECK IF TRANSMIT POWER DIFFERS BY EACH ROUTER IN NCS BUILDING!!!!!!!!!
    # get transmit power
    ptx = estimate_transmit_power()

    # order: 2.4GHz * 3 , 5.0GHz * 3 (top-bottom / each router)
    AP_list = {
        'H1': [AccessPoint('7A:E0', 2.4, (0, 0), ptx), AccessPoint('7A:E1', 2.4, (0, 0), ptx),
               AccessPoint('7A:E3', 2.4, (0, 0), ptx), AccessPoint('7A:F0', 5.0, (0, 0), ptx),
               AccessPoint('7A:F1', 5.0, (0, 0), ptx), AccessPoint('7A:F3', 5.0, (0, 0), ptx)],

        'H2': [AccessPoint('77:00', 2.4, (0, 0), ptx), AccessPoint('77:01', 2.4, (0, 0), ptx),
               AccessPoint('77:03', 2.4, (0, 0), ptx), AccessPoint('77:10', 5.0, (0, 0), ptx),
               AccessPoint('77:11', 5.0, (0, 0), ptx), AccessPoint('77:13', 5.0, (0, 0), ptx)],

        'H3': [AccessPoint('FC:80', 2.4, (0, 0), ptx), AccessPoint('FC:82', 2.4, (0, 0), ptx),
               AccessPoint('FC:83', 2.4, (0, 0), ptx), AccessPoint('FC:90', 5.0, (0, 0), ptx),
               AccessPoint('FC:92', 5.0, (0, 0), ptx), AccessPoint('FC:93', 5.0, (0, 0), ptx)],

        'H4': [AccessPoint(':60', 2.4, (0, 0), ptx), AccessPoint(':61', 2.4, (0, 0), ptx),
               AccessPoint(':63', 2.4, (0, 0), ptx), AccessPoint(':70', 5.0, (0, 0), ptx),
               AccessPoint(':71', 5.0, (0, 0), ptx), AccessPoint(':73', 5.0, (0, 0), ptx)],
        # GET THE MAC ADDRESS AGAIN!
        # GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!
        # GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!
        # GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!# GET THE MAC ADDRESS AGAIN!

        'P1': [AccessPoint('7A:C0', 2.4, (0, 0), ptx), AccessPoint('7A:C1', 2.4, (0, 0), ptx),
               AccessPoint('7A:C3', 2.4, (0, 0), ptx), AccessPoint('7A:D0', 5.0, (0, 0), ptx),
               AccessPoint('7A:D1', 5.0, (0, 0), ptx), AccessPoint('7A:D3', 5.0, (0, 0), ptx)],

        'P2': [AccessPoint('7B:A0', 2.4, (0, 0), ptx), AccessPoint('7B:A1', 2.4, (0, 0), ptx),
               AccessPoint('7B:A3', 2.4, (0, 0), ptx), AccessPoint('7B:B0', 5.0, (0, 0), ptx),
               AccessPoint('7B:B1', 5.0, (0, 0), ptx), AccessPoint('7B:B3', 5.0, (0, 0), ptx)],

        'L1': [AccessPoint('85:E0', 2.4, (0, 0), ptx), AccessPoint('85:E2', 2.4, (0, 0), ptx),
               AccessPoint('85:E3', 2.4, (0, 0), ptx), AccessPoint('85:F0', 5.0, (0, 0), ptx),
               AccessPoint('85:F2', 5.0, (0, 0), ptx), AccessPoint('85:F3', 5.0, (0, 0), ptx)],

        'L2': [AccessPoint('7C:00', 2.4, (0, 0), ptx), AccessPoint('7C:01', 2.4, (0, 0), ptx),
               AccessPoint('7C:03', 2.4, (0, 0), ptx), AccessPoint('7C:10', 5.0, (0, 0), ptx),
               AccessPoint('7C:11', 5.0, (0, 0), ptx), AccessPoint('7C:13', 5.0, (0, 0), ptx)],

        'S1': [AccessPoint('85:A0', 2.4, (0, 0), ptx), AccessPoint('85:A1', 2.4, (0, 0), ptx),
               AccessPoint('85:A3', 2.4, (0, 0), ptx), AccessPoint('85:B0', 5.0, (0, 0), ptx),
               AccessPoint('85:B1', 5.0, (0, 0), ptx), AccessPoint('85:B3', 5.0, (0, 0), ptx)],

        'S2': [AccessPoint('E1:60', 2.4, (0, 0), ptx), AccessPoint('E1:62', 2.4, (0, 0), ptx),
               AccessPoint('E1:63', 2.4, (0, 0), ptx), AccessPoint('E1:70', 5.0, (0, 0), ptx),
               AccessPoint('E1:72', 5.0, (0, 0), ptx), AccessPoint('E1:73', 5.0, (0, 0), ptx)]}
    trilateration = Trilateration()

    # -------------------------------------------------------------------------------------------------------

    while True:
        # Receive data from the device (JSON + PARSE + SAVE TO LOCAL VARIABLES)
        wifi_data = WifiSignalParse()  # pase the device's all the near wifi data
        wifi_data.receive_data()
        wifi_data.find_dominant_signal(3)  # 3 most strongest wifi signals

        data = {}
        current_ap_list = []
        for ap in wifi_data.strongest_signal_list:
            data['dist'] = trilateration.get_estimated_distance(ptx, ap.rssi)
            position = get_pos_with_group(AP_list, ap.group, ap.bssid)
            if position == -1:
                print('Wi-fi not found')
                break
            data['x'] = position.x
            data['y'] = position.y
            current_ap_list.append(data)

        x_coord, y_coord = trilateration.get_position(current_ap_list)
        print(x_coord, y_coord)
        break  # for testing purpose
