import unittest, binanceWrapper

class TestBinanceWrapper(unittest.TestCase):
	pass

	def testPing(self):
		self.assertTrue(binanceWrapper.ping())

	def testMakeRequest(self):
		res = binanceWrapper._makeRequest('GET', f'{binanceWrapper.API_PATH}/api/v3/ping')
		self.assertEqual(res, {})





if __name__ == '__main__':
	unittest.main()