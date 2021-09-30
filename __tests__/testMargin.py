import binanceWrapper
import unittest

class TestMarginEndpoints(unittest.TestCase):

	@classmethod
	def setUp(cls):
		import json
		with open('keys.json', 'r') as f:
			keys = json.loads(f.read())
			binanceWrapper.Keys.API.set(keys['API'])
			binanceWrapper.Keys.SECRET.set(keys['SECRET'])

	def testMarginAccount(self):
		self.assertEqual(type(binanceWrapper.marginAccount()), dict)

	