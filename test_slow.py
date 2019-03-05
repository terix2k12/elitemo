import unittest
import elite

class MyTestSuite(unittest.TestCase):

	def dtest_elite_deals_real(self):
		self.elite.markets = assets.markets("listings.csv")
		self.elite.stations = assets.stations("stations.json")
		self.elite.systems = assets.systems("systems_populated.json")

		station = self.elite.findStationLike("Russell Ring")[0]
		marketId = station["id"]

		system = self.elite.system(id=station["system_id"])
		proxies = self.elite.proxies(15, system)

		self.assertEqual(len(proxies), 77)

		deals = self.elite.bestdeals(marketId, proxies, 200)

		self.assertEqual(deals, (596000, [(68, '29', 992, 200), (1265, '24', 1988, 200)]))

	def stest_compute(self):
		self.elite.commodities = assets.commodities("commodities.json")

		data = {}
		data['cargohold'] = 100
		data['landingpad'] = "L"
		data['jumprange'] = 13
		data['maxhops'] = 5

		step0 = {}
		step0[u'systemId'] = "Eravate"
		step0["stationId"] = "Russell Ring"
		data[u'route'] = []
		data[u'route'].append(step0)

		result = self.elite.compute(data)

		self.assertEqual(result, "hi")

	# make this somehow only executed in SLOW tests
	def slow_test_assets_markets_big(self):
		markets = assets.markets("listings.csv")
		self.assertEqual(len(markets), 53899)

if __name__ == "__main__":
	unittest.main()