import binanceWrapper, os
import unittest
from dotenv import load_dotenv

# @unittest.skip
class TestMarginEndpoints(unittest.TestCase):

	def setUp(cls):
			load_dotenv()
			binanceWrapper.setKeys(os.getenv('APIKEY'), os.getenv('SECRETKEY'))

	def testMarginAccount(self):
		self.assertEqual(type(binanceWrapper.marginAccount()), dict)

	def testMarginBalance(self):
		res = binanceWrapper.marginBalance()
		self.assertEqual(type(res), float)
		print(f"Binance Balance: {res}")