import unittest

import elite
import entities
import assets

class MyTestSuite(unittest.TestCase):

	def setUp(self):
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
		deals = elite.bestdeals(market, proxies, 20)
		self.assertEqual(deals, (4800, [(4615,"30",50,20),(4857,"12",190,20)] ))

	def test_elite_deals_return2(self):
		entities.markets = assets.markets("test/test-deal-return2.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = elite.bestdeals(market, proxies, 100)
		self.assertEqual(deals, (35490, [(4615, '32', 433, 30), (4615, '30', 50, 70), (4857, '12', 190, 100)]))

	def test_elite_deals_return3(self):
		entities.markets = assets.markets("test/test-deal-return3.csv")
		market = 4615
		proxies = [1081, 4857]
		deals = elite.bestdeals(market, proxies, 150)
		self.assertEqual(deals, (9000, [(4615, 0, 0, 0), (1081, '12', 60, 150)]))

	def test_compute(self):
		data = {}
		data["cargohold"] = ""
		data["landingpad"] = ""
		data["jumprange"] = ""
		data["maxhops"] = ""
		data["route"] = []
		step0 = {}
		step0["system"] = "Eravate"
		step0["station"] = "Russell Ring"
		data["route"].append( step0 )

		elite.compute(data)

if __name__ == "__main__":
	unittest.main()