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





if __name__ == '__main__':
	unittest.main()