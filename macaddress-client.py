#!/usr/bin/python3

import requests
import sys
import os

# Constants
API_KEY_ENV_NAME = 'MACADDRESS_API_KEY'
MACADDRESS_URL = 'https://api.macaddress.io/v1'

if len(sys.argv) != 2:
    print("MAC address not passed", file=sys.stderr)
    sys.exit(1)

if API_KEY_ENV_NAME not in os.environ:
    print("API key missing (env variable: " + API_KEY_ENV_NAME + ")", file=sys.stderr)
    sys.exit(1)

auth_token = os.environ.get(API_KEY_ENV_NAME)
query = sys.argv[1]

parameters = { 'output': 'vendor', 'search': query }
headers = {'X-Authentication-Token': auth_token }
try:
    req = requests.get(MACADDRESS_URL, params=parameters, headers=headers)
except Exception as exc:
    print("Request failed when connecting: " + str(exc), file=sys.stderr)
    sys.exit(255)

if req.status_code != 200:
    print("Request failed with HTTP code " + req.status_code, file=sys.stderr)
    sys.exit(255)

if not req.text:
    result = "(Unknown vendor)"
else:
    result = req.text


print(result, end='')
