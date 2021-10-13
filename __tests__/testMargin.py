import binanceWrapper, os
import unittest
from dotenv import load_dotenv

class TestMarginEndpoints(unittest.TestCase):

	def setUp(cls):
			load_dotenv()
			binanceWrapper.Keys.API.set(os.getenv('APIKEY'))
			binanceWrapper.Keys.SECRET.set(os.getenv('SECRETKEY'))

	def testMarginAccount(self):
		self.assertEqual(type(binanceWrapper.marginAccount()), dict)

	