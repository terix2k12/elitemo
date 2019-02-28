import unittest

import elite
from assets import assets

class TestAsset(unittest.TestCase):

	def setUp(self):
		self.assets = assets()
		self.assets.listing = "mini-listings.csv"

	def test_assets_markets(self):
		markets = self.assets.markets()
		self.assertEqual(len(markets), 2)

	def test_assets_commodities(self):
		commodities = self.assets.commodities()
		self.assertEqual(len(commodities), 355)

	# TODO category long run?
	def tes_assets_bigdata(self):
		rows = self.assets.loadCSV("listings.csv")
		self.assertEqual(len(rows), 5664189)

	# this is inefficient
	def tes_assets_bigmarkets(self):
		self.assets.listing = "listings.csv" 
		self.assets.markets()

		self.assertEqual(len(markets), 5664189)