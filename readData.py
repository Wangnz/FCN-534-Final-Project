import json
import numpy as np
import subprocess
import os
import platform
from datetime import datetime


def get_access_points():
    # cmd = "netsh wlan show networks mode=bssid"  # Windows (TO USE, DIFF PARSING REQUIRED)
    cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -s"  # Mac
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


def get_filename(timestamp):
    cur_date = timestamp.date()
    cur_time = timestamp.time()

    # YYMMDD HHMMSS format
    filename = "{0}{1:02d}{2:02d}_{3:02d}{4:02d}{5:02d}".format(str(cur_date.year)[-2:], cur_date.month,
                                                                cur_date.day, cur_time.hour,
                                                                cur_time.minute,
                                                                cur_time.second)
    return filename


def as_record_format(ap_data):
    return "{0:2s} {1} {2} {3}\n".format(ap_data['RSSI'], ap_data['GROUP'], ap_data['BSSID'], ap_data['SSID'])


def platform_check():
    operating_system = platform.system().lower()
    if operating_system != 'darwin':
        print("Mac OS platform required")
        exit(1)


if __name__ == "__main__":
    # only run it under mac OS
    platform_check()

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
    timestamp = datetime.now()
    filename_record_time = get_filename(timestamp)
    iter_cnt = 0

    if not os.path.exists('./Record'):
        os.makedirs('./Record')

    with open('./Record/Record(' + filename_record_time + ').txt', 'w') as f:
        f.write(str(timestamp) + '\n')
        f.write("START\n")
        while True:
            iter_cnt += 1
            f.write("-----------------------------------------------------------------Iter " + str(iter_cnt) + "\n")
            try:
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

                # convert into recording format and record signals
                for ap_data in sorted_ap_list:
                    ap_data_record = as_record_format(ap_data)
                    f.write(ap_data_record)
            except Exception as e:
                f.write("[ERROR] : " + str(e.message) + "\n")
                print("[ERROR] :%s" % str(e.message))
                break

        f.write("FINISH")
