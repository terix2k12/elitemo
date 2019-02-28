import unittest

from elite import elite
from assets import assets

class MyTestSuite(unittest.TestCase):

	def setUp(self):
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

	def test_loadListing(self):
		self.elite.markets = assets().loadMarkets()

		self.assertEqual(len(self.elite.markets), 7)

	def test_loadMarket(self):
		a = assets()
		self.elite.markets = a.loadMarkets()
		self.elite.commodities = a.loadCommodities()

		stationId = 1

		market = self.elite.loadMarket(stationId)

		self.assertEqual(len(market), 7)

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
	

	# (elite.commodities, elite.systems, elite.stations) = assets().loadAssets()

	

	unittest.main()