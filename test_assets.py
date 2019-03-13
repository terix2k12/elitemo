import unittest
import assets

class TestAsset(unittest.TestCase):

	def test_assets_markets(self):
		markets = assets.markets("test/test-markets.csv")
		self.assertEqual(len(markets), 4)

	def test_assets_commodities(self):
		commodities = assets.commodities("commodities.json")
		self.assertEqual(len(commodities), 355)

	def test_assets_systems(self):
		systems = assets.systems("test/test-systems.json")
		# print [s["id"] for s in systems]
		self.assertEqual(len(systems), 5)		

	def test_assets_stations(self):
		stations = assets.stations("test/test-stations.json")
		# print [(s["name"],s["id"]) for s in stations]
		self.assertEqual(len(stations), 20)

	def slow_test_assets_doPickle(self):
		stations = assets.stations("stations.json")
		assets.doPickle(stations, "stations.pic")

	def slow_test_assets_unPickle(self):
		stations = assets.unPickle("stations.pic")
		self.assertEqual(len(stations), 68598)

if __name__ == "__main__":
	unittest.main()