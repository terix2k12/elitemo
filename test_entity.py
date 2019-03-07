import unittest
import assets
import entities

class TestEntities(unittest.TestCase):

    def setUp(self):
        entities.markets = assets.markets("test/test-markets.csv")
        entities.systems = assets.systems("test/test-systems.json")
        entities.stations = assets.stations("test/test-stations.json")
        entities.commodities = assets.commodities("commodities.json")


    def test_entities_system_name(self):
        system = entities.system(name="Eravate")
        self.assertEqual(system["id"], 4615)

    def test_entities_system_id(self):
        system = entities.system(id=4615)
        self.assertEqual(system["name"], "Eravate")

    def test_entities_system_id_str(self):
        system = entities.system(id="4615")
        self.assertEqual(system["name"], "Eravate")


    def test_entities_station_id(self):
        station = entities.station(id=232)
        self.assertEqual(station["name"], "Sylvester City")

    def test_entities_station_id_str(self):
         station = entities.station(id="232")
         self.assertEqual(station["name"], "Sylvester City")

    def test_entities_station_name(self):
        station = entities.station(name="Sylvester City")
        self.assertEqual(station["id"], 232)


    def test_entities_market(self):
        market = entities.market(1)
        self.assertEqual(len(market), 7)


    def test_entities_commodity_id(self):
        commodity = entities.commodity(id=5)
        self.assertEqual("Clothing", commodity["name"])

    def test_entities_commodity_id_str(self):
        commodity = entities.commodity(id="5")
        self.assertEqual("Clothing", commodity["name"])

    def test_entities_commodity_name(self):
        commodity = entities.commodity(name="Clothing")
        self.assertEqual(5, commodity["id"])


    def test_entities_commodity_at_market_id(self):
        market = entities.market(1)
        commodity = entities.commodity(market=market, id=5)
        self.assertEqual("123", commodity["buy_price"])

    def test_entities_commodity_at_market_id_str(self):
        market = entities.market(1)
        commodity = entities.commodity(market=market, id="5")
        self.assertEqual("123", commodity["buy_price"])

    def test_entities_commodity_market_name(self):
        market = entities.market(1)
        commodity = entities.commodity(market=market, name="Clothing")
        self.assertEqual("123", commodity["buy_price"])


    def test_entities_system_stations_id(self):
        system = entities.system(id=4615)
        stations = entities.station(system=system)
        self.assertEqual(len(stations), 11)


if __name__ == "__main__":
    unittest.main()