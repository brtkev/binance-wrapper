import binanceWrapper, os
import unittest
from dotenv import load_dotenv

# @unittest.skip
class Spot(unittest.TestCase):

	def setUp(cls):
			load_dotenv()
			binanceWrapper.setKeys(os.getenv('APIKEY'), os.getenv('SECRETKEY'))

	def newOCO(self):
		print(binanceWrapper.newOCO(symbol = 'BTCUSDT', side = 'BUY', quantity=1, price=200, stopPrice=250, 
        stopLimitPrice=150, stopLimitTimeInForce= 'FOK'))                                               
    