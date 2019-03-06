import unittest
import assets

class TestAsset(unittest.TestCase):

	def test_assets_markets(self):
		markets = assets.markets("test/test-markets.csv")
		self.assertEqual(len(markets), 2)

	def test_assets_commodities(self):
		commodities = assets.commodities("commodities.json")
		self.assertEqual(len(commodities), 355)

	def test_assets_systems(self):
		systems = assets.systems("test/test-systems.json")
		# print [s["id"] for s in systems]
		self.assertEqual(len(systems), 4)		

	def test_assets_stations(self):
		stations = assets.stations("test/test-stations.json")
		# print [(s["name"],s["id"]) for s in stations]
		self.assertEqual(len(stations), 20)

if __name__ == "__main__":
	unittest.main()