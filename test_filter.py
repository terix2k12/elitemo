import unittest
import assets
import entities
import filter

class TestFilter(unittest.TestCase):
    def setUp(self):
        entities.markets = assets.markets("test/test-markets.csv")
        entities.systems = assets.systems("test/test-systems.json")
        entities.stations = assets.stations("test/test-stations.json")
        entities.commodities = assets.commodities("commodities.json")
        
    def test_filter_proxies(self):
        eravate = entities.system(id=4615)
        markets = filter.stations(system=eravate, options={"ly":15})
        self.assertEqual(len(markets), 0)

    def test_filter_system(self):
        system = entities.system(name="Eravate")
        proximity = filter.stations(system=system, options={"ly":15})
        self.assertEqual(len(proximity), 0)

if __name__ == "__main__":
    unittest.main()