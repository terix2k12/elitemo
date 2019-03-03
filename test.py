import unittest

from elite import elite
import assets

class MyTestSuite(unittest.TestCase):

	def setUp(self):
		self.elite = elite()
		self.elite.markets = assets.markets("test/test-markets.csv")
		self.elite.systems = assets.systems("test/test-systems.json")
		self.elite.stations = assets.stations("test/test-stations.json")

	#def inputData(self):

#
#	#	return data
#
	#def test_simplecompute(self):
	#	data = self.inputData()	
	#	result = self.elite.compute(data)
	#	self.assertEqual(len(result[u'route']), 2)

	def test_elite_market(self):
		marketId = 1
		items = self.elite.market(marketId)
		self.assertEqual(len(items), 7)

	def test_elite_commodity(self):
		self.elite.commodities = assets.commodities("commodities.json")
		commodityId = 5	
		commodityName = "Clothing"
		commodity = self.elite.commodity(commodityId)
		self.assertEqual(commodityName, commodity["name"])

	def test_market_item(self):
		marketId = 1
		market = self.elite.market(marketId)
		commodityId = 5	
		commodity = self.elite.item(market, commodityId)
		self.assertEqual(commodityId, int(commodity["commodity_id"]))

	def test_market_itemTime(self):
		market = self.elite.market(1)
		item = self.elite.item(market, 5)
		utc = item["collected_at"]
		self.assertEqual('2019-02-17 18:07:43', self.elite.time(utc) )

	def test_market_itemAge(self):		
		market = self.elite.market(1)
		item = self.elite.item(market, 5)
		utc = item["collected_at"]
		self.assertEqual(4, self.elite.age(utc) )

	def test_market_sort(self):
		stationId = 1
		market = self.elite.market(stationId)
		self.elite.sortMarket(market, "demand")
		self.assertEqual(market[0]["demand"], "8898")

	def test_elite_system_name(self):
		system = self.elite.system(name="Eravate")
		self.assertEqual(system["name"], "Eravate")

	def test_elite_system_id(self):
		system = self.elite.system(id=4615)
		self.assertEqual(system["name"], "Eravate")

	def test_elite_station_id(self):
		station = self.elite.station(id=232)
		self.assertEqual(station["name"], "Sylvester City")

	def test_elite_proximity(self):
		system = self.elite.system(name="Eravate")
		proximity = self.elite.proximity(15, system)
		# print([sys["name"] for sys in proximity])
		self.assertEqual(len(proximity), 3)

	def test_elite_children(self):
		systemId = 4615 
		stations = self.elite.children(systemId)
		self.assertEqual(len(stations), 11)

	def test_elite_proxies(self):
		system = self.elite.system(id=4615)
		markets = self.elite.proxies(15, system)

		self.assertEqual(len(markets), 16)

	def test_elite_deals_simple(self):
		self.elite.markets = assets.markets("test/test-deal-simple.csv")
		market1 = self.elite.market(1)
		market2 = self.elite.market(2)

		deals = self.elite.deals(market1, market2)

		self.assertEqual(deals[0], ("7", 673, 200))

	def test_elite_deals_return1(self):
		self.elite.markets = assets.markets("test/test-deal-return1.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = self.elite.bestdeals(market, proxies, 20)
		self.assertEqual(deals, (4800, [(4615,"30",50,20),(4857,"12",190,20)] ))

	def test_elite_deals_return2(self):
		self.elite.markets = assets.markets("test/test-deal-return2.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = self.elite.bestdeals(market, proxies, 100)
		self.assertEqual(deals, (35490, [(4615, '32', 433, 30), (4615, '30', 50, 70), (4857, '12', 190, 100)]))

	def test_elite_deals_return3(self):
		self.elite.markets = assets.markets("test/test-deal-return3.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = self.elite.bestdeals(market, proxies, 150)
		self.assertEqual(deals, (9000, [(4615, 0, 0, 0), (1081, '12', 60, 150)]))

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

	def test_compute(self):
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

if __name__ == "__main__":
	unittest.main()