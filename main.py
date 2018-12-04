import json

from flask import Flask
from flask import send_from_directory
from flask import jsonify

from wifisignal import WifiSignalParse
from accesspoint import AccessPoint
from trilateration import Trilateration
from trilateration import estimate_transmit_power

def load_ap_map():
  with open('access_points.json') as ap_json_data:
    ap_json_list = json.load(ap_json_data)

    result = {}
    for ap_json in ap_json_list:
      result[ap_json['name']] = ap_from_json(ap_json)

  return result

def ap_from_json(ap):
  result = []
  ptx = estimate_transmit_power()
  for bssid in ap['2g']:
    result.append(AccessPoint(bssid.upper(), 2.4, (ap['x'], ap['y']), ptx))

  for bssid in ap['5g']:
    result.append(AccessPoint(bssid.upper(), 5.0, (ap['x'], ap['y']), ptx))

  return result

def get_position():
  wifi_data = WifiSignalParse()
  global AP_map
  wifi_data.receive_data(AP_map)

  trilateration = Trilateration()
  pos, routers, estimates = trilateration.trilaterate(wifi_data, AP_map)
  return {
    'pos': {
      'x': pos[0],
      'y': pos[1],
    },
    'routers': routers,
    'estimates': estimates
  }

# define flask app
app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
  return send_from_directory("static", "index.html")

@app.route("/update")
def update():
  data = get_position()
  # print "update", data
  return jsonify(data)

def get_data():
  global test_data
  global test_data_index
  data = test_data[test_data_index]
  test_data_index += 1
  if test_data_index >= len(test_data):
    test_data_index = 0
  return data

# access point map
AP_map = load_ap_map()