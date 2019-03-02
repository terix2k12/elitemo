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
#	#	data = {}
#	#	data['cargohold'] = 288
#	#	data['landingpad'] = "L"
#	#	data['jumprange'] = 13
#	#	data['maxhops'] = 5
#	#
#	#	step0 = {}
#	#	step0[u'systemId'] = u'LHS 3447'
#	#	step0["stationId"] = 1
#	#	data[u'route'] = []
#	#	data[u'route'].append(step0)
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

		print [sys["name"] for sys in proximity]

		self.assertEqual(len(proximity), 3)

	def test_elite_deals(self):
		self.elite.markets = assets.markets("test/test-markets.csv")
		market1 = self.elite.market(1)
		market2 = self.elite.market(2)

		deals = self.elite.deals(market1, market2)

		self.assertEqual(len(deals), 7)

	def test_elite_deals_eravate(self):
		self.elite.markets = assets.markets("test/best-deal-one-way.csv")
		# self.elite.commodities = assets.commodities()
		# self.elite.systems = assets.systems()
 
		#system = self.elite.system("Eravate")
		#proximity = self.elite.proximity(15, system)
#
#		#print proximity
#
#		#deals = self.elite.bestdeals(system, proximity)
#
#		#print deals
#
		#self.assertEqual(len(deals), 7)


	#def test_findBestCommodityAtStation(self):
#
#	#	data = self.inputData()
#
	#	currentStation = data["route"].
	
#	def test_orderPresentCommodities(self):
#		station = {}
#		station["name"] = "Merope"
#		commodities = []
#
#		commodities.append(hydrogenFuel)
#		station["commodities"] = commodities
#		stations = []
#		stations.append(station)
#
#		pass


if __name__ == "__main__":
	unittest.main()