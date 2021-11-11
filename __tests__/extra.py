import binanceWrapper
import unittest


class Extra(unittest.TestCase):


    def symbolHistorialKlines(self):
        import time
        startTime = '10 oct 2020'
        endTime = '5 mar 2021'
        res = binanceWrapper.extra.symbolHistorialKlines('XRPUSDT', '1h', startTime, endTime)
        self.assertGreater(len(res), 500)
