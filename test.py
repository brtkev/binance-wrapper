import unittest, logging
logging.basicConfig(filename='test.log', format='\n[%(asctime)s] - %(levelname)s - {%(filename)s:%(lineno)d} - %(name)s - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')

from __tests__ import *


if __name__ == '__main__':
	unittest.main()