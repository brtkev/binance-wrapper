import unittest, binanceWrapper

class TestBinanceWrapper(unittest.TestCase):
	pass

	def testPing(self):
		self.assertTrue(binanceWrapper.ping())

	def test_MakeRequest(self):
		res = binanceWrapper._makeRequest('GET', f'{binanceWrapper.API_PATH}/api/v3/ping')
		self.assertEqual(res, {})

	@unittest.expectedFailure
	def test_requestError(self):
		binanceWrapper._requestError("response text", 0, {"params" : "some info"})

class TestInfoEndpoints(unittest.TestCase):

	def testSymbolPrice(self):
		priceDict = binanceWrapper.symbolPrice()
		self.assertIs(type(priceDict), list)

		symbol = 'BTCUSDT'
		priceDict = binanceWrapper.symbolPrice(symbol)
		self.assertIs(priceDict['symbol'], symbol)

	def testSymbolLastKlines(self):
		symbol = 'BTCUSDT'
		res = binanceWrapper.symbolLastKlines(symbol, '1m')
		self.assertIs(type(res), list)
		self.assertIs(len(res), 500)




if __name__ == '__main__':
	unittest.main()