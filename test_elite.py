import unittest
import json

import elite
import entities
import assets

class TestElite(unittest.TestCase):

	def setUp(self):
		entities.reset()
		entities.markets = assets.markets("test/test-markets.csv")
		entities.systems = assets.systems("test/test-systems.json")
		entities.stations = assets.stations("test/test-stations.json")
		entities.commodities = assets.commodities("commodities.json")

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

		deals = elite.deals(market1, market2)

		self.assertEqual(deals[0], ("7", 673, 200))

	def test_elite_deals_return1(self):
		entities.markets = assets.markets("test/test-deal-return1.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = elite.bestdealReturn(market, proxies, 20)
		self.assertEqual(deals, (4800, [(4615,"30",50,20),(4857,"12",190,20)] ))

	def test_elite_deals_return2(self):
		entities.markets = assets.markets("test/test-deal-return2.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = elite.bestdealReturn(market, proxies, 100)
		self.assertEqual(deals, (35490, [(4615, '32', 433, 30), (4615, '30', 50, 70), (4857, '12', 190, 100)]))

	def test_elite_deals_return3(self):
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

	def test_compute_11a(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Eravate"
		result = elite.compute(self.data)
		expected = {'cargohold': 16, "steps": [{"system": "Eravate", "instructions": [[(3, 2, '5', 150, 10)]]}] }
		self.assertEqual(expected, result)

	def test_compute_11a_noresult(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Adw System"
		result = elite.compute(self.data)
		expected = {'cargohold': 16, "steps": [{"system": "Adw System", "instructions": []}] }
		self.assertEqual(result, expected)

	def test_compute_11b(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Eravate"
		step0["station"] = "Russell Ring"
		result = elite.compute(self.data)
		expected = {'cargohold': 16, 'steps': [{'station': 'Russell Ring', 'system': 'Eravate', 'instructions': []}]}
		self.assertEqual(result, expected)

	def test_compute_12a(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Eravate"
		step0["station"] = "Russell Ring"
		mission1 = {}
		mission1["type"] = "deliver"
		mission1["destination"] = "Chomsky Terminal"
		mission1["commodity"] = "Clothing"
		mission1["amount"] = 12
		step0["missions"] = [mission1]
		result = elite.compute(self.data)
		# TODO verify test....
		expected = {'cargohold': 16, 'steps': [{'station': 'Russell Ring', 'system': 'Eravate', 'missions': [{'amount': 12, 'destination': 'Chomsky Terminal', 'type': 'deliver', 'commodity': 'Clothing'}], 'instructions': [[]]}]}
		self.assertEqual(result, expected)

	def test_compute_12b(self):
		self.computeSetup()
		step0 = self.data["steps"][0]
		step0["system"] = "Eravate"
		step0["station"] = "Russell Ring"
		mission1 = {}
		mission1["type"] = "source"
		mission1["commodity"] = "Clothing"
		mission1["amount"] = 8
		mission1["reward"] = 120000
		step0["missions"] = [mission1]
		# TODO test with maxjumps=1 not very useful
		result = elite.compute(self.data)
		expected = {'cargohold': 16, 'steps': [{'station': 'Russell Ring', 'system': 'Eravate', 'missions': [{'amount': 8, 'reward': 120000, 'type': 'source', 'commodity': 'Clothing'}], 'instructions': [(3, 1, 5, 120000, 8)]}]}
		self.assertEqual(result, expected)


if __name__ == "__main__":
	unittest.main()