import unittest
from assets import assets

class TestAsset(unittest.TestCase):

	def setUp(self):
		self.assets = assets()

	def test_assets_markets(self):
		markets = self.assets.markets("test/test-markets.csv")
		self.assertEqual(len(markets), 2)

	def test_assets_commodities(self):
		commodities = self.assets.commodities("commodities.json")
		self.assertEqual(len(commodities), 355)

	def test_assets_systems(self):
		systems = self.assets.systems("test/test-systems.json")
		# print [s["id"] for s in systems]
		self.assertEqual(len(systems), 4)		

	def test_assets_stations(self):
		stations = self.assets.systems("test/test-stations.json")
		# print [s["name"] for s in stations]
		self.assertEqual(len(stations), 20)

	# make this somehow only executed in SLOW tests
	def slow_test_assets_markets_big(self):
		markets = self.assets.markets("listings.csv")
		self.assertEqual(len(markets), 53899)