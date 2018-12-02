#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import numpy as np
import subprocess
import types

def get_access_points():
    # cmd = "netsh wlan show networks mode=bssid" # all the APs I communicate with
    cmd = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport -s"  # the one I'm connected to
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (out, _) = proc.communicate()
    return out

def get_data(infile):

    input_file = open(infile, mode="r")

    infile_content = input_file.readlines()

    # 定义空列表存储临时数据，将同一组数据存储在同一列表中

    list_temp = []
    for each in infile_content:
        list_temp.append(each.split())
    print(list_temp)
    print(len(list_temp))

    # 将嵌套的列表转换成json格式的字典
    # dict_temp =  dict(list_temp)
    # print(dict_temp)
    # print(len(dict_temp))

    # 关闭文件
    input_file.close()

    #截取前三列
    list_SSID = [i[0] for i in list_temp]
    list_BSSID = [i[1] for i in list_temp]
    list_RSSI = [i[2] for i in list_temp]

    #合并数组, 删除首行并json化
    list_before = np.c_[list_SSID, list_BSSID, list_RSSI]
    list_before = np.delete(list_before, 0, axis=0)
    print list_before

    list_js = json.dumps(list_before)
    print list_js

    with open('test3.txt', 'w') as f:
        f.write(str(list_temp))


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



def SignalSort(x, y, z):
    signals = [Signal(ssid, bssid, rssi) for (ssid, bssid, rssi) in [(x, y, z)]]
    signals.sort(cmp=None, key=lambda x: x.rssi, reverse=False)
    for element in signals:
        print element.ssid, ":", element.bssid, ":", element.rssi

if __name__ == "__main__":
    # get_data("SomeFile.txt")
    while True:
        res = get_access_points()
        res = res.split('\n')
        final = []
        for index in xrange(1, len(res)-1):
            dict = {}
            res_2 = res[index].strip().split(' ')
            # if res_2[0].startswith('cs_'):
            if res_2[0].startswith('cs_'):
                dict['SSID'] = res_2[0]
                dict['BSSID'] = res_2[1]
                dict['RSSI'] = res_2[2]
                final.append(dict)
                final_json = json.dumps(final)

        # for kebi in final:
        #     s = Signal(kebi['SSID'], kebi['BSSID'], kebi['RSSI'])
        #     print s
        final_sort = sorted(final, key=lambda e: e['RSSI'], reverse=False)
        # print(final_sort)
        # print final_sort[0]['BSSID']
        # Cut out the strongest routers from our list
        router_list = []
        router_list_final = []
        last = []
        router_group = []

        for index in range(59):
            router_list.append(final_sort[index])
            hallway1 = ['7a:e0', '7a:e1', '7a:e3', '7a:f0', '7a:f1', '7a:f3']
            hallway2 = ['77:00', '77:01', '77:03', '77:10', '77:11', '77:13']
            hallway3 = ['fc:80', 'fc:82', 'fc:83', 'fc:90', 'fc:92', 'fc:93']
            hallway4 = ['77:60', '77:61', '77:63', '77:70', '77:71', '77:73']
            lobby1 = ['85:e0', '85:e2', '85:e3', '85:f0', '85:f2', '85:f3']
            lobby2 = ['7c:13', '7c:11', '7c:10', '7c:03', '7c:01', '7c:00']
            professor_hallway1 = ['7a:c0', '7a:c1', '7a:c3', '7a:d0', '7a:d1', '7a:d3']
            professor_hallway2 = ['7b:a0', '7b:a1', '7b:a3', '7b:b0', '7b:b1', '7b:b3']
            seminar_room1 = ['85:a0', '85:a1', '85:a3', '85:b0', '85:b1', '85:b3']
            seminar_room2 = ['e1:60', 'e1:62', 'e1:63', 'e1:70', 'e1:72', 'e1:73']
            # name_list3 = ['23:b0', '23:b1', '23:b2']
            # name_list1 = ['1f:52', '1f:51', '1f:50']
            # name_list4 = ['85:50', '85:52', '85:53']

            res = router_list[index]
            for index2 in range(6):
                if hallway1[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('H1')
                    # router_list_final.append(router_list[index])
                    # result = router_list[index]
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'H1'})
                elif hallway2[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('H2')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'H2'})
                elif hallway3[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('H3')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'H3'})
                elif hallway4[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('H4')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'H4'})
                elif lobby1[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('L1')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'L1'})
                elif lobby2[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('L2')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'L2'})
                elif professor_hallway1[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('P1')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'P1'})
                elif professor_hallway2[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('P2')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'P2'})
                elif seminar_room1[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('S1')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'S1'})
                elif seminar_room2[index2] in router_list[index]['BSSID'][-5:]:
                    # router_group.append('S2')
                    # router_list_final.append(router_list[index])
                    last.append({'SSID': res['SSID'], 'BSSID': res['BSSID'], 'RSSI': res['RSSI'], 'Group': 'S2'})

        # Strongest 3
        # router_group = sorted(list(set(router_group))[:3])
        # router_group = sorted(list(set(router_group)))
        # print router_group, len(router_group)
        # print router_list_final
        print last, len(last)
        # last_json = json.dumps(last, ensure_ascii=False)
        # loaded_json = json.loads(json.dumps(last_json))

        # print loaded_json, type(loaded_json)