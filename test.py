import unittest

from elite import elite
from assets import assets

class MyTestSuite(unittest.TestCase):

	def setUp(self):
		self.assets = assets()
		self.elite = elite()

	def inputData(self):
		data = {}
		data['cargohold'] = 288
		data['landingpad'] = "L"
		data['jumprange'] = 13
		data['maxhops'] = 5
	
		step0 = {}
		step0[u'systemId'] = u'LHS 3447'
		step0["stationId"] = 1
		data[u'route'] = []
		data[u'route'].append(step0)

		return data

	def test_simplecompute(self):
		data = self.inputData()	

		result = self.elite.compute(data)
	
		self.assertEqual(len(result[u'route']), 2)

	def test_assets_markets(self):
		self.elite.markets = self.assets.markets()
		self.assertEqual(len(self.elite.markets), 2)

	def test_assets_commodities(self):
		self.elite.commodities = self.assets.loadCommodities()
		self.assertEqual(len(self.elite.commodities), 355)

	def test_elite_market(self):
		self.elite.markets = self.assets.markets()
		marketId = 1

		market = self.elite.market(marketId)

		self.assertEqual(len(market.items), 7)

	def test_elite_commodity(self):
		self.elite.commodities = self.assets.loadCommodities()
		commodityId = 5	
		commodityName = "Clothing"

		commodity = self.elite.commodity(commodityId)

		self.assertEqual(commodityName, commodity["name"])

	def test_market_item(self):
		self.elite.markets = self.assets.markets()
		marketId = 1
		market = self.elite.market(marketId)
		commodityId = 5	

		commodity = market.item(commodityId)

		self.assertEqual(commodityId, int(commodity["commodity_id"]))

	def test_market_itemTime(self):
		self.elite.markets = self.assets.markets()
		market = self.elite.market(1)
		item = market.item(5)

		utc = item["collected_at"]

		self.assertEqual('2019-02-17 18:07:43', self.elite.time(utc) )

	def test_market_itemAge(self):
		self.elite.markets = self.assets.markets()
		market = self.elite.market(1)
		item = market.item(5)

		utc = item["collected_at"]

		self.assertEqual(4, self.elite.age(utc) )

	def test_market_sort(self):
		self.elite.markets = self.assets.markets()
		stationId = 1
		market = self.elite.market(stationId)

		market.sortFor("demand")

		self.assertEqual(market.items[0]["demand"], "8898")

	def test_elite_deals(self):
		self.elite.markets = self.assets.markets()
		self.elite.commodities = self.assets.loadCommodities()
		market1 = self.elite.market(1)
		market2 = self.elite.market(2)

		deals = self.elite.deals(market1, market2)

		self.assertEqual(len(deals), 7)


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