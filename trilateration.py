import numpy as np
import time
import math
from accesspoint import AccessPoint
from wifisignal import WifiSignalParse


# --------------------------------------------------------------------------------------------------------------------

class Trilateration:

    def __init__(self):
        pass

    def line(self, p1, p2):
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0] * p2[1] - p2[0] * p1[1])
        return A, B, -C

    def intersection(self, L1, L2):
        D = L1[0] * L2[1] - L1[1] * L2[0]
        Dx = L1[2] * L2[1] - L1[1] * L2[2]
        Dy = L1[0] * L2[2] - L1[2] * L2[0]
        if D != 0:
            x = Dx / D
            y = Dy / D
            return x, y
        else:
            return False

    # Euclidean distance
    def calc_dist(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Average three points(center1,2, & centroid of intersection point)
    def calc_avg_pos(self, center_point_1_x, center_point_1_y, center_point_2_x, center_point_2_y, intersection_point_x,
                     intersection_point_y):
        return ((center_point_1_x + center_point_2_x + intersection_point_x) / 3,
                (center_point_1_y + center_point_2_y + intersection_point_y) / 3)

    # param : ap1, ar2 = data dictionary
    def ap_circle_condition_check(self, ap1, ap2):
        dist = self.calc_dist((ap1['x'], ap1['y']), (ap2['x'], ap2['y']))  # distance of the two circles
        radius_1 = ap1['dist']  # AP_1's radius
        radius_2 = ap2['dist']  # AP_2 's radius

        # inner circle check(one circle is inside the other)
        if dist < abs(radius_1 - radius_2):
            print('Inner circle')
            if radius_1 > radius_2:
                return 0, (ap2['x'], ap2['y'])
            else:
                return 0, (ap1['x'], ap1['y'])

        # if radius_1 > dist or radius_2 > dist: # partial inner
        #     return False

        # separate circle check
        if dist > radius_1 + radius_2:
            print('Seperate circle')
            return -1, -1

        # complete coincide circle check
        if dist == 0 and radius_1 == radius_2:
            print('Coincide circle')
            return 0, (ap1['x'], ap1['y'])

        return 1, -1

    # param : ap1, ar2 = data dictionary
    def get_intersecting_points(self, ap1, ap2):
        dist = self.calc_dist((ap1['x'], ap1['y']), (ap2['x'], ap2['y']))  # distance of the two circles
        radius_1 = ap1['dist']  # AP_1's radius
        radius_2 = ap2['dist']  # AP_2 's radius

        sub_x = ap2['x'] - ap1['x']
        sub_y = ap2['y'] - ap1['y']
        tmp = (radius_1 * radius_1 - radius_2 * radius_2 + dist * dist) / (2 * dist)
        tmp_2 = math.sqrt(radius_1 * radius_1 - tmp * tmp)
        xm = ap1['x'] + tmp * sub_x / dist
        ym = ap1['y'] + tmp * sub_y / dist
        pt_x1 = xm + tmp_2 * sub_y / dist
        pt_x2 = xm - tmp_2 * sub_y / dist
        pt_y1 = ym - tmp_2 * sub_x / dist
        pt_y2 = ym + tmp_2 * sub_x / dist

        return (pt_x1, pt_y1), (pt_x2, pt_y2)

    # param: anchor_ap (AP that has the most strong RSSI signal / the circle that is to be compared with every other circls)
    # param: ap_list (target APs that are going to be searched)
    def get_position_votes(self, anchor_ap, ap_list):
        estimated_position_votes = []
        for target_ap in ap_list:
            (ap_check, ap_check_res) = self.ap_circle_condition_check(anchor_ap, target_ap)
            if ap_check == -1:
                print("> the circle does not qualify : skip checking")
                continue
            else:
                intersection_centroid = (-99999.0, -99999.0)
                final_centroid = (-99999.0, -99999.0)
                if ap_check == 0:
                    final_centroid = ap_check_res
                else:
                    intersect_point_1, intersect_point_2 = self.get_intersecting_points(anchor_ap, target_ap)
                    ap_center_line = self.line((anchor_ap['x'], anchor_ap['y']), (target_ap['x'], target_ap['y']))
                    intersect_point_line = self.line(intersect_point_1, intersect_point_2)

                    # intersecting in only one point
                    if intersect_point_1 == intersect_point_2:
                        intersection_centroid = intersect_point_1
                        if anchor_ap['dist'] > target_ap['dist']:
                            final_centroid = (target_ap['x'], target_ap['y'])
                        else:
                            final_centroid = (anchor_ap['x'], anchor_ap['y'])
                    else:
                        intersection_centroid = self.intersection(ap_center_line, intersect_point_line)
                        final_centroid = self.calc_avg_pos(anchor_ap['x'], anchor_ap['y'], target_ap['x'],
                                                           target_ap['y'], intersection_centroid[0],
                                                           intersection_centroid[1])
                if final_centroid != (-99999.0, -99999.0):
                    estimated_position_votes.append(final_centroid)

        return estimated_position_votes


def get_estimated_distance(transmit_power, rssi):
    k = -27.55
    freq = 5200.0  # doesn't matter as long as it is consistent to get_transmit_power()'s frequency value
    dist = 10 ** ((transmit_power - rssi - k - 20.0 * math.log10(freq)) / 20.0)

    return dist


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


def get_pos_with_group(ap_list, target_bssid):
    coord = -1
    for data in ap_list:
        if target_bssid.endswith(data.bssid):
            coord = data.pos
            break

    return coord


def get_pos_data(AP_list, ptx, ap):
    data = {}
    data['dist'] = get_estimated_distance(ptx, ap.rssi)
    position = get_pos_with_group(AP_list[ap.group], ap.bssid)
    if position == -1:
        print('Such WiFi signal not found')
        return None
    data['x'] = position.x
    data['y'] = position.y

    return data


# using normal distribution + standard deviation to remove outliers
def get_position(votes):
    mean = np.mean(votes, axis=0)
    std = np.std(votes, axis=0)
    sigma_factor = 1

    votes_without_outliers = []

    for vote_points in votes:
        x = vote_points[0]
        y = vote_points[1]

        x_mean = mean[0]
        y_mean = mean[1]
        x_std = std[0]
        y_std = std[1]

        # mean +- sigma <>
        if x_mean - sigma_factor * x_std <= x and x <= x_mean + sigma_factor * x_std:
            if y_mean - sigma_factor * y_std <= y and y <= y_mean + sigma_factor * y_std:
                votes_without_outliers.append((x, y))

    return np.mean(votes_without_outliers, axis=0)


if __name__ == "__main__":

    # CHECK IF TRANSMIT POWER DIFFERS BY EACH ROUTER IN NCS BUILDING!!!!!!!!!
    # get transmit power
    ptx = estimate_transmit_power()

    # order: 2.4GHz * 3 , 5.0GHz * 3 (top-bottom / each router)
    AP_list = {
        'H1': [AccessPoint('7A:E0', 2.4, (0.0, 9.1440), ptx), AccessPoint('7A:E1', 2.4, (0.0, 9.1440), ptx),
               AccessPoint('7A:E3', 2.4, (0.0, 9.1440), ptx), AccessPoint('7A:F0', 5.0, (0.0, 9.1440), ptx),
               AccessPoint('7A:F1', 5.0, (0.0, 9.1440), ptx), AccessPoint('7A:F3', 5.0, (0.0, 9.1440), ptx)],

        'H2': [AccessPoint('77:00', 2.4, (0.0, 0.0), ptx), AccessPoint('77:01', 2.4, (0.0, 0.0), ptx),
               AccessPoint('77:03', 2.4, (0.0, 0.0), ptx), AccessPoint('77:10', 5.0, (0.0, 0.0), ptx),
               AccessPoint('77:11', 5.0, (0.0, 0.0), ptx), AccessPoint('77:13', 5.0, (0.0, 0.0), ptx)],

        'H3': [AccessPoint('FC:80', 2.4, (0.0, -14.6050), ptx), AccessPoint('FC:82', 2.4, (0.0, -14.6050), ptx),
               AccessPoint('FC:83', 2.4, (0.0, -14.6050), ptx), AccessPoint('FC:90', 5.0, (0.0, -14.6050), ptx),
               AccessPoint('FC:92', 5.0, (0.0, -14.6050), ptx), AccessPoint('FC:93', 5.0, (0.0, -14.6050), ptx)],

        'H4': [AccessPoint('77:60', 2.4, (0.0, -27.4320), ptx), AccessPoint('77:61', 2.4, (0.0, -27.4320), ptx),
               AccessPoint('77:63', 2.4, (0.0, -27.4320), ptx), AccessPoint('77:70', 5.0, (0.0, -27.4320), ptx),
               AccessPoint('77:71', 5.0, (0.0, -27.4320), ptx), AccessPoint('77:73', 5.0, (0.0, -27.4320), ptx)],

        'P1': [AccessPoint('7A:C0', 2.4, (21.4884, 21.6662), ptx), AccessPoint('7A:C1', 2.4, (21.4884, 21.6662), ptx),
               AccessPoint('7A:C3', 2.4, (21.4884, 21.6662), ptx), AccessPoint('7A:D0', 5.0, (21.4884, 21.6662), ptx),
               AccessPoint('7A:D1', 5.0, (21.4884, 21.6662), ptx), AccessPoint('7A:D3', 5.0, (21.4884, 21.6662), ptx)],

        'P2': [AccessPoint('7B:A0', 2.4, (10.5410, 21.6662), ptx), AccessPoint('7B:A1', 2.4, (10.5410, 21.6662), ptx),
               AccessPoint('7B:A3', 2.4, (10.5410, 21.6662), ptx), AccessPoint('7B:B0', 5.0, (10.5410, 21.6662), ptx),
               AccessPoint('7B:B1', 5.0, (10.5410, 21.6662), ptx), AccessPoint('7B:B3', 5.0, (10.5410, 21.6662), ptx)],

        'L1': [AccessPoint('85:E0', 2.4, (0.0, 31.5976), ptx), AccessPoint('85:E2', 2.4, (0.0, 31.5976), ptx),
               AccessPoint('85:E3', 2.4, (0.0, 31.5976), ptx), AccessPoint('85:F0', 5.0, (0.0, 31.5976), ptx),
               AccessPoint('85:F2', 5.0, (0.0, 31.5976), ptx), AccessPoint('85:F3', 5.0, (0.0, 31.5976), ptx)],

        'L2': [AccessPoint('7C:00', 2.4, (0.0, 17.0434), ptx), AccessPoint('7C:01', 2.4, (0.0, 17.0434), ptx),
               AccessPoint('7C:03', 2.4, (0.0, 17.0434), ptx), AccessPoint('7C:10', 5.0, (0.0, 17.0434), ptx),
               AccessPoint('7C:11', 5.0, (0.0, 17.0434), ptx), AccessPoint('7C:13', 5.0, (0.0, 17.0434), ptx)],

        # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # CHECK THE MAC ADDRESS FOR S1 AND S2!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # CHECK THE MAC ADDRESS FOR S1 AND S2# CHECK THE MAC ADDRESS FOR S1 AND S2
        # CHECK THE MAC ADDRESS FOR S1 AND S2# CHECK THE MAC ADDRESS FOR S1 AND S2

        'S2': [AccessPoint('85:A0', 2.4, (-5.6896, 21.6281), ptx), AccessPoint('85:A1', 2.4, (-5.6896, 21.6281), ptx),
               AccessPoint('85:A3', 2.4, (-5.6896, 21.6281), ptx), AccessPoint('85:B0', 5.0, (-5.6896, 21.6281), ptx),
               AccessPoint('85:B1', 5.0, (-5.6896, 21.6281), ptx), AccessPoint('85:B3', 5.0, (-5.6896, 21.6281), ptx)],

        'S1': [AccessPoint('E1:60', 2.4, (-10.8966, 27.7241), ptx), AccessPoint('E1:62', 2.4, (-10.8966, 27.7241), ptx),
               AccessPoint('E1:63', 2.4, (-10.8966, 27.7241), ptx), AccessPoint('E1:70', 5.0, (-10.8966, 27.7241), ptx),
               AccessPoint('E1:72', 5.0, (-10.8966, 27.7241), ptx),
               AccessPoint('E1:73', 5.0, (-10.8966, 27.7241), ptx)]}
    trilateration = Trilateration()

    while True:
        # Receive data from the device (JSON + PARSE + SAVE TO LOCAL VARIABLES)
        wifi_data = WifiSignalParse()  # pase the device's all the near wifi data
        wifi_data.receive_data()
        wifi_data.find_dominant_signal(3)  # 3 most strongest wifi signals
        anchor_signal = wifi_data.anchor_signal

        APs_signal_pos_data = []
        anchor_signal_pos_data = get_pos_data(AP_list, ptx, anchor_signal)
        for ap in wifi_data.strongest_signal_list:
            data = get_pos_data(AP_list, ptx, ap)
            if data is not None:
                APs_signal_pos_data.append(data)

        estimated_position_votes = trilateration.get_position_votes(anchor_signal_pos_data, APs_signal_pos_data)

        # print("Anchor : ", anchor_signal_pos_data)
        # print("APs : ", APs_signal_pos_data)
        # print("Result : ", estimated_position_votes)
        print("Outlier filtered result :", get_position(estimated_position_votes))
        break  # for testing purpose
