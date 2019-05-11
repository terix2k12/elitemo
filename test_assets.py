import unittest
import assets
import os

# For benchmarks:
import time
import sys

class TestAsset(unittest.TestCase):

	def test_assets_markets(self):
		markets = assets.markets("test/test-markets.csv")
		self.assertEqual(len(markets), 4)

	def test_assets_commodities(self):
		commodities = assets.commodities("res/commodities.json")
		self.assertEqual(len(commodities), 355)

	def test_assets_systems(self):
		systems = assets.systems("test/test-systems.json")
		self.assertEqual(len(systems), 5)		

	def test_assets_stations(self):
		stations = assets.stations("test/test-stations.json")
		self.assertEqual(len(stations), 20)

	def slow_test_asset_update(self):
		filename = "commodities.json"
		success = assets.update(filename)
		exists = os.path.isfile(filename)
		self.assertEqual(success and exists, True)

	def slow_test_asset_update_fail(self):
		filename = "xzynono"
		success = assets.update(filename)
		exists = os.path.isfile(filename)
		self.assertEqual(not (success and exists), False)		

	def slow_test_asset_install(self):
		assets.update("res/commodities.json", True)
		assets.update("res/stations.json", True)
		assets.update("res/systems_populated.json", True)
		assets.update("res/listings.csv", True)

	def slow_test_assets_doPickle(self):
		stations = assets.stations("stations.json")
		assets.doPickle(stations, "stations.pic")

	def slow_test_assets_unPickle(self):
		stations = assets.unPickle("stations.pic")
		self.assertEqual(len(stations), 68598)

	def test_profile_and_improve(self):
		
		start = time.time()
		inmemoryjson = assets.loadJSONl("testbig", "res/stations.jsonl")
		dicbytes = sys.getsizeof(inmemoryjson)

		print "Structure size is " + str( dicbytes / 1024 ) + " kB"
		# print "Total size is " + str( allbytes / 1024 ) + " kB"

		end = time.time()		
		print("loading time: " + str(end - start) )

		start = time.time()

		systems = {}
		for r in inmemoryjson:
			systems[r["id"]] = r
		
		print "Structure size is " + str( sys.getsizeof(systems) / 1024 ) + " kB"

		end = time.time()
		print("iteration time: " + str(end - start) )

		self.assertEqual(len(inmemoryjson), 68768)

if __name__ == "__main__":
	unittest.main()