import unittest, binanceWrapper


class TestInfoEndpoints(unittest.TestCase):

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
		res = binanceWrapper.server_time()
		self.assertIn('serverTime', res)

	def testAccountCoints(self):
		binanceWrapper.accountCoins()	