import unittest

import elite
from assets import assets

class TestAsset(unittest.TestCase):

	def setUp(self):
		self.assets = assets()

	def test_assets_markets(self):
		markets = self.assets.markets()
		self.assertEqual(len(markets), 2)

	def test_assets_commodities(self):
		commodities = self.assets.commodities()
		self.assertEqual(len(commodities), 355)

	# TODO category long run?
	def tes_assets_bigdata(self):
		self.assets.loadCSV("listings.csv")