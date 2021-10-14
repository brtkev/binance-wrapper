from binanceWrapper.info import accountCoins
import unittest, binanceWrapper, os

class TestInfoEndpoints(unittest.TestCase):

	@classmethod
	def setUp(cls):
		cls.symbol = 'BTCUSDT'

		from dotenv import load_dotenv
		load_dotenv()
		binanceWrapper.setKeys(os.getenv('APIKEY'), os.getenv('SECRETKEY'))
		

	def testSymbolPrice(self):
		priceDict = binanceWrapper.symbolPrice()
		self.assertIs(type(priceDict), list)

		priceDict = binanceWrapper.symbolPrice(self.symbol)
		self.assertEqual(priceDict['symbol'], self.symbol)

	def testSymbolLastKlines(self):
		res = binanceWrapper.symbolLastKlines(self.symbol, '1m')
		self.assertIs(type(res), list)
		self.assertEqual(len(res), 500)

		res = binanceWrapper.symbolLastKlines(self.symbol, '1m', 10)
		self.assertEqual(len(res), 10)

	def testSymbolKlines(self):
		import time
		startTime = int(time.mktime(time.strptime("2020", "%Y"))) 
		endTime = startTime + 1000 * 60 * 60
		print(time.gmtime(endTime))
		klines = binanceWrapper.symbolKlines(self.symbol, '1h', 1000, startTime * 1000)
		firstBarStartTime = time.gmtime(klines[0][0]/1000)
		
		self.assertEqual(firstBarStartTime, time.gmtime(startTime))
		self.assertEqual(time.gmtime(endTime), time.gmtime(klines[-1][0] / 1000))
		self.assertEqual(len(klines), 1000)

	def testServerTime(self):
		res = binanceWrapper.serverTime()
		self.assertIn('serverTime', res)

	def testAccountCoins(self):
		binanceWrapper.accountCoins()
			
	def testAccountInfo(self):
		binanceWrapper.accountInfo()