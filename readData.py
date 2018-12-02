import json
import numpy as np
import subprocess


def get_access_points():
    cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -s"
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, _) = proc.communicate()

    return out


# get which group the router(=AP) is in
# param: type=dict(list), type=string
def get_ap_group(AP_list, target_bssid):
    group = 'X'
    for ap_group in AP_list.keys():
        if target_bssid in AP_list[ap_group]:
            group = ap_group
            break

    return group


if __name__ == "__main__":
    AP_list = {
        'H1': ['7a:e0', '7a:e1', '7a:e3', '7a:f0', '7a:f1', '7a:f3'],
        'H2': ['77:00', '77:01', '77:03', '77:10', '77:11', '77:13'],
        'H3': ['fc:80', 'fc:82', 'fc:83', 'fc:90', 'fc:92', 'fc:93'],
        'H4': ['77:60', '77:61', '77:63', '77:70', '77:71', '77:73'],
        'L1': ['85:e0', '85:e2', '85:e3', '85:f0', '85:f2', '85:f3'],
        'L2': ['7c:00', '7c:01', '7c:03', '7c:10', '7c:11', '7c:13'],
        'P1': ['7a:c0', '7a:c1', '7a:c3', '7a:d0', '7a:d1', '7a:d3'],
        'P2': ['7b:a0', '7b:a1', '7b:a3', '7b:b0', '7b:b1', '7b:b3'],
        'S1': ['85:a0', '85:a1', '85:a3', '85:b0', '85:b1', '85:b3'],
        'S2': ['e1:60', 'e1:62', 'e1:63', 'e1:70', 'e1:72', 'e1:73']
    }
    while True:
        raw_ap_list = get_access_points()
        raw_ap_list_2 = raw_ap_list.split('\n')
        filtered_ap_list = []
        for index in xrange(1, len(raw_ap_list_2)):
            signal_data = {}
            raw_ap = raw_ap_list_2[index].strip().split(' ')

            # excluding signals that are not useful (e.g. printers)
            if raw_ap[0].startswith('cs_'):
                signal_data['SSID'] = raw_ap[0]
                signal_data['BSSID'] = raw_ap[1][-5:].upper()
                signal_data['RSSI'] = raw_ap[2]
                group_res = get_ap_group(AP_list, raw_ap[1][-5:])
                if group_res == 'X':
                    print("Such WiFi signal not found")
                signal_data['GROUP'] = group_res
                filtered_ap_list.append(signal_data)
                # final_json = json.dumps(final)

        # sort by signal strength (RSSI)
        sorted_ap_list = sorted(filtered_ap_list, key=lambda e: e['RSSI'], reverse=False)
