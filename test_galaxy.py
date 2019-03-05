import unittest
import assets
import entities
import galaxy

class TestFilter(unittest.TestCase):

    def setUp(self):
        entities.markets = assets.markets("test/test-markets.csv")
        entities.systems = assets.systems("test/test-systems.json")
        entities.stations = assets.stations("test/test-stations.json")
        entities.commodities = assets.commodities("commodities.json")

    def test_galaxy_stations(self):
        system = entities.system(id=4615)
        opt = { "ly":15, "landingpad":"L" }
        stations = galaxy.stations(system=system, options=opt)
        self.assertEqual(len(stations), 16)

    def test_galaxy_system(self):
        system = entities.system(name="Eravate")
        opt = { "ly":15 }
        proximity = galaxy.systems(system=system, options=opt)
        self.assertEqual(len(proximity), 3)

if __name__ == "__main__":
    unittest.main()