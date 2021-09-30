from binanceWrapper.info import accountCoins
import unittest, binanceWrapper


class TestInfoEndpoints(unittest.TestCase):

	@classmethod
	def setUp(cls):
		import json
		with open('keys.json', 'r') as f:
			keys = json.loads(f.read())
			binanceWrapper.Keys.API.set(keys['API'])
			binanceWrapper.Keys.SECRET.set(keys['SECRET'])

	def testSymbolPrice(self):
		priceDict = binanceWrapper.symbolPrice()
		self.assertIs(type(priceDict), list)

		symbol = 'BTCUSDT'
		priceDict = binanceWrapper.symbolPrice(symbol)
		self.assertEqual(priceDict['symbol'], symbol)

	def testSymbolLastKlines(self):
		symbol = 'BTCUSDT'
		res = binanceWrapper.symbolLastKlines(symbol, '1m')
		self.assertIs(type(res), list)
		self.assertEqual(len(res), 500)

		res = binanceWrapper.symbolLastKlines(symbol, '1m', 10)
		self.assertEqual(len(res), 10)

	def testServerTime(self):
		res = binanceWrapper.serverTime()
		self.assertIn('serverTime', res)

	def testAccountCoins(self):
		accCoins = binanceWrapper.accountCoins()
		self.assertEqual(type(accCoins), list)
		for coin in accCoins:
			with self.subTest(coin = coin):
				self.assertEqual(type(coin), dict)
			
	def testAccountInfo(self):
		accInfo = binanceWrapper.accountInfo()
		import json
		with open('file.json', 'w') as f:
			f.write(json.dumps(accInfo))