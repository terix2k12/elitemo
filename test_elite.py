import unittest
import json

import elitecore
import elite

import entities
import assets

class TestElite(unittest.TestCase):

	def setUp(self):
		entities.reset()
		entities.markets = assets.markets("test/test-markets.csv")
		entities.systems = assets.systems("test/test-systems.json")
		entities.stations = assets.stations("test/test-stations.json")
		entities.commodities = assets.commodities("res/commodities.json")

	def test_market_itemTime(self):
		market = entities.market(1)
		item = entities.commodity(market, 5)
		utc = item["collected_at"]
		self.assertEqual('2019-02-17 18:07:43', elite.time(utc) )

	def test_market_itemAge(self):		
		market = entities.market(1)
		item = entities.commodity(market, 5)
		utc = item["collected_at"]
		self.assertEqual(4, elite.age(utc) )

	def test_market_sort(self):
		market = entities.market(1)
		elite.sortMarket(market, "demand")
		self.assertEqual(market[0]["demand"], "8898")

	def test_elite_deals_simple(self):
		entities.markets = assets.markets("test/test-deal-simple.csv")
		market1 = entities.market(1)
		market2 = entities.market(2)

		deals = elitecore.getdeals(market1, market2)

		self.assertEqual(deals[0], ("7", 673, 200))

	def xtest_elite_deals_return1(self):
		entities.markets = assets.markets("test/test-deal-return1.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = elite.bestdealReturn(market, proxies, 20)
		self.assertEqual(deals, (4800, [(4615,"30",50,20),(4857,"12",190,20)] ))

	def xtest_elite_deals_return2(self):
		entities.markets = assets.markets("test/test-deal-return2.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = elite.bestdealReturn(market, proxies, 100)
		self.assertEqual(deals, (35490, [(4615, '32', 433, 30), (4615, '30', 50, 70), (4857, '12', 190, 100)]))

	def xtest_elite_deals_return3(self):
		entities.markets = assets.markets("test/test-deal-return3.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = elite.bestdealReturn(market, proxies, 150)
		self.assertEqual(deals, (9000, [(4615, 0, 0, 0), (1081, '12', 60, 150)]))

	def computeSetup(self):
		entities.systems = assets.systems("test/test-systems2.json")
		entities.stations = assets.stations("test/test-stations2.json")
		entities.markets = assets.markets("test/test-markets2.csv")

		self.data = {}
		self.data["cargohold"] = 16
		self.data["steps"] = []
		step0 = {}
		step0["instructions"] = []
		self.data["steps"].append( step0 )

	def xtest_compute_d(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Eravate"
		step0["station"] = "Russell Ring"
		mission1 = {}
		mission1["type"] = "Delivery"
		mission1["station"] = "Chomsky Terminal"
		mission1["system"] = "Frigaha"
		mission1["commodity"] = "Clothing"
		mission1["amount"] = 12
		mission1["reward"] = 150000
		step0["missions"] = [mission1]
		result = elite.compute(self.data)
		expected = {'cargohold': 16, 'steps': [{'station': 'Russell Ring', 'system': 'Eravate', 'missions': [{'commodity': 'Clothing', 'system': 'Frigaha', 'amount': 12, 'station': 'Chomsky Terminal', 'reward': 150000, 'type': 'Delivery'}], 'instructions': [(u'Russell Ring', u'Chomsky Terminal', 5, 150000, 0, 12)]}]}
		self.assertEqual(result, expected)

	def xtest_compute_s(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Eravate"
		step0["station"] = "Russell Ring"
		mission1 = {}
		mission1["type"] = "Source"
		mission1["commodity"] = "Clothing"
		mission1["amount"] = 8
		mission1["reward"] = 120000
		step0["missions"] = [mission1]
		# TODO test with maxjumps=1 not very useful
		result = elite.compute(self.data)
		expected =  {'cargohold': 16, 'steps': [{'station': 'Russell Ring', 'system': 'Eravate', 'missions': [{'amount': 8, 'reward': 120000, 'type': 'Source', 'commodity': 'Clothing'}], 'instructions': [(u'Russell Ring', u'Bluford Station', u'Clothing', 0, 0, 0)]}]} 
		self.assertEqual(result, expected)

	def xtest_compute_i(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Eravate"
		step0["station"] = "Russell Ring"
		mission1 = {}
		mission1["type"] = "Intel"
		mission1["system"] = "Frigaha" 
		mission1["station"] = "Lawson Orbital"
		mission1["reward"] = 120000
		step0["missions"] = [mission1]
		result = elite.compute(self.data)
		expected = {'cargohold': 16, 'steps': [{'station': 'Russell Ring', 'system': 'Eravate', 'missions': [{'station': 'Lawson Orbital', 'type': 'Intel', 'system': 'Frigaha', 'reward': 120000}], 'instructions': [(u'Russell Ring', u'Lawson Orbital', 0, 120000, 0, 0)]}]}
		self.assertEqual(result, expected)

if __name__ == "__main__":
	unittest.main()