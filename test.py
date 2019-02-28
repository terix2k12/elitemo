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

	def test_loadAllMarkets(self):
		self.elite.markets = self.assets.loadMarkets()

		self.assertEqual(len(self.elite.markets), 7)

	def test_loadSpecificMarket(self):
		self.elite.markets = self.assets.loadMarkets()

		stationId = 1

		market = self.elite.loadMarket(stationId)

		self.assertEqual(len(market), 7)

	def test_loadCommodity(self):
		self.elite.commodities = self.assets.loadCommodities()

		commodityId = 5	
		commodityName = "Clothing"

		commodity = self.elite.getCommodity(commodityId)

		self.assertEqual(commodityName, commodity["name"])

	def test_showCommoditiesPerMarket(self):
		self.elite.markets = self.assets.loadMarkets()
		self.elite.commodities = self.assets.loadCommodities()
		
		stationId = 1

		market = self.elite.loadMarket(stationId)

		print market

		self.assertEqual(False, True)


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