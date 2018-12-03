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
  wifi_data.receive_data()

  global AP_map
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

@app.route("/model")
def model():
  model = get_model()
  return jsonify(model)

@app.route("/update")
def update():
  data = get_position()
  print "update", data
  return jsonify(data)

# @app.route("/update")
# def update():
#   data = get_data()
#   import time
#   time.sleep(1)
#   return jsonify(data)

def get_data():
  global test_data
  global test_data_index
  data = test_data[test_data_index]
  test_data_index += 1
  if test_data_index >= len(test_data):
    test_data_index = 0
  return data

test_data_index = 0
test_data = [
  {
    "pos" : {
      "x" : 0,
      "y" : 0,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 1,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 2,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 3,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 4,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
   {
    "pos" : {
      "x" :  -0.5,
      "y" : 5,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 6,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 7,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 8,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 9,
    },
    "routers": [
     "h3",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 10,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 11,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 12,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 13,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 14,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 15,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 16,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 17,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 18,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 19,
    },
    "routers": [
     "l2",
     "h2",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 20,
    },
    "routers": [
     "l2",
     "l1",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 21,
    },
    "routers": [
     "l2",
     "l1",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 22,
    },
    "routers": [
     "l2",
     "l1",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 23,
    },
    "routers": [
     "l2",
     "l1",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 24,
    },
    "routers": [
     "l2",
     "l1",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 25,
    },
    "routers": [
     "l2",
     "l1",
     "h1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 26,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 27,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 28,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
  {
    "pos" : {
      "x" :  -0.5,
      "y" : 29,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
  {
    "pos" : {
      "x" : -6,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
  {
    "pos" : {
      "x" : -7,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
  {
    "pos" : {
      "x" : -8,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
   {
    "pos" : {
      "x" : -9,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
   {
    "pos" : {
      "x" : -10,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
   {
    "pos" : {
      "x" : -11,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
   {
    "pos" : {
      "x" : -12,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
   {
    "pos" : {
      "x" : -13,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
   {
    "pos" : {
      "x" : -14,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
   {
    "pos" : {
      "x" : -15,
      "y" : 30,
    },
    "routers": [
     "l2",
     "l1",
     "s1",
    ],
  },
]

# access point map
AP_map = load_ap_map()