"""
pyexample.

An example python library.
"""

__version__ = "1.0.2"
__author__ = 'Kevin Breto'

import binanceWrapper.utils as utils
from binanceWrapper.utils import _makeRequest, _requestError, ping, Keys
from binanceWrapper.info import *
from binanceWrapper.exceptions import *
from binanceWrapper.margin import *

def setKeys(api, secret):
  Keys.API.set(api)
  Keys.SECRET.set(secret)

