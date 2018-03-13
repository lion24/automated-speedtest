from lib.speedtestprovider.speedtest import SpeedtestProvider

import unittest

class TestProviders(unittest.TestCase):
	def setUp(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		self.driver = webdriver.Chrome(chrome_options=options)
		self.driver.implicitly_wait(30)
		self.driver.maximize_window()
		self.providers = []