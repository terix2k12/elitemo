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
        self.assertEqual(system["name"], "Eravate")

    def test_entities_system_id(self):
        system = entities.system(id=4615)
        self.assertEqual(system["name"], "Eravate")

    def test_entities_station_id(self):
        station = entities.station(id=232)
        self.assertEqual(station["name"], "Sylvester City")

    def test_entities_station_id_str(self):
         station = entities.station(id="232")
         self.assertEqual(station["name"], "Sylvester City")

    def test_entities_market(self):
        marketId = 1
        market = entities.market(marketId)
        self.assertEqual(len(market), 7)

    def test_entities_commodity_Id_Int(self):
        commodityId = 5    
        commodityName = "Clothing"
        commodity = entities.commodity(id=commodityId)
        self.assertEqual(commodityName, commodity["name"])

    def test_entities_commodity_Id_String(self):
        commodityId = "5"    
        commodityName = "Clothing"
        commodity = entities.commodity(id=commodityId)
        self.assertEqual(commodityName, commodity["name"])

    def test_entities_commodity_Name(self):
        commodityId = 5    
        commodityName = "Clothing"
        commodity = entities.commodity(name=commodityName)
        self.assertEqual(commodityId, commodity["id"])

    def test_entities_commodity_market_id(self):
        market = entities.market(1)
        commodity = entities.commodity(market, id=5)
        self.assertEqual("123", commodity["buy_price"])

# TODO This function doesn't work
#    def xtest_entities_commodity_market_name(self):
#        market = entities.market(1)
#        commodity = entities.commodity(market, name="Clothing")
#        self.assertEqual("123", int(commodity["buy_price"]))

#    def test_entities_system_stations_id(self):
#        system = entities.system(id=4615)
#        stations = entities.station(system=system)
#        self.assertEqual(len(stations), 11)

# TODO does not work right now
#    def test_entities_system_stations_name(self):
#        stations = entities.station(system="Eravate")
#        self.assertEqual(len(stations), 11)

if __name__ == "__main__":
    unittest.main()