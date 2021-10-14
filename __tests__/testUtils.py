import unittest, binanceWrapper

@unittest.skip
class TestUtils(unittest.TestCase):

	def testPing(self):
		self.assertTrue(binanceWrapper.ping())

	def test_MakeRequest(self):
		res = binanceWrapper._makeRequest('GET', f'{binanceWrapper.API_PATH}/api/v3/ping')
		self.assertEqual(res, {})

	@unittest.expectedFailure
	def test_requestError(self):
		binanceWrapper._requestError("response text", 0, {"params" : "some info"})

@unittest.skip
class TestKeys(unittest.TestCase):
	@classmethod
	def setUp(cls):
		cls.testKey = binanceWrapper.utils.Key()

	def testGetKey(self):
		self.assertRaises(binanceWrapper.BinanceKeyError, self.testKey.get) #if empty

		key = binanceWrapper.utils.Key("123") #if not empty
		self.assertEqual(key.get(), "123")

	def testSetKey(self):
		self.testKey.set('123')
		self.assertEqual(self.testKey.get(), "123")

	def testKeys(self):
		binanceWrapper.Keys.API.set('123')
		self.assertEqual(binanceWrapper.Keys.API.get(), '123')
		binanceWrapper.Keys.SECRET.set('abc')
		self.assertEqual(binanceWrapper.Keys.SECRET.get(), 'abc')