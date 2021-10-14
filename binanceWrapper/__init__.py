"""
pyexample.

An example python library.
"""
import json
with open("version.json", "r") as f:
  version = json.loads(f.read())
__version__ = version['version']
__author__ = version['author']

import binanceWrapper.utils as utils
from binanceWrapper.utils import _makeRequest, _requestError, ping, Keys
from binanceWrapper.info import *
from binanceWrapper.exceptions import *
from binanceWrapper.margin import *

def setKeys(api, secret):
  Keys.API.set(api)
  Keys.SECRET.set(secret)

