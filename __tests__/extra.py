import binanceWrapper
import unittest


class Extra(unittest.TestCase):


    def symbolHistorialKlines(self):
        import time

        startTime =  int(time.mktime(time.strptime('10 oct 2020', "%d %b %Y")))
        endTime = int(time.mktime(time.strptime('5 mar 2021', "%d %b %Y")))
        res = binanceWrapper.extra.symbolHistorialKlines('XRPUSDT', '1h', startTime, endTime)
        self.assertGreater(len(res), 500)
