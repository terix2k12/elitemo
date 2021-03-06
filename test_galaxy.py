import unittest
import assets
import entities
import galaxy

class TestGalaxy(unittest.TestCase):

    def setUp(self):
        entities.reset()
        entities.markets = assets.markets("test/test-markets.csv")
        entities.systems = assets.systems("test/test-systems.json")
        entities.stations = assets.stations("test/test-stations.json")
        entities.commodities = assets.commodities("res/commodities.json")

    def test_padsize(self):
        self.assertEquals(3, galaxy.padsize("L"))
        self.assertEquals(2, galaxy.padsize("M"))
        self.assertEquals(1, galaxy.padsize(""))


    def test_galaxy_proximity_system(self):
        system = entities.system(name="Eravate")
        opt = { "ly" : 15 }
        systems = galaxy.proximity(system=system, options=opt)
        self.assertEqual(len(systems), 3)

    def test_galaxy_proximity_station(self):
        station = entities.station(name="Russell Ring")
        opt = { "ly" : 15 }
        systems = galaxy.proximity(station=station, options=opt)
        self.assertEqual(len(systems), 3)


    def test_galaxy_hubs_system(self):
        system = entities.system(id=4615)
        opt = { "ly": 15 }
        stations = galaxy.hubs(system=system, options=opt)
        self.assertEqual(len(stations), 16)

    def test_galaxy_hubs_station(self):
        station = entities.station(name="Russell Ring")
        opt = { "ly": 15, "landingpad":"L" }
        stations = galaxy.hubs(station=station, options=opt)
        self.assertEqual(len(stations), 9)

    def test_galaxy_hubs_expectedCommodity(self):
        station = entities.station(name="Russell Ring")
        commodity = entities.commodity(id=8)
        opt = { "commodity": [ (commodity["id"], 12) ] }
        stations = galaxy.hubs(station=station, options=opt)
        self.assertEqual(len(stations), 1)
        self.assertEqual(stations[0]["name"], "Green Keep")

    # TODO expected more than one commodity


    def slow_test_create_galaxy_minipickle(self):
        entities.reset()
        entities.systems = assets.systems("res/systems_populated.json")
        entities.stations = assets.systems("res/stations.json")
        entities.markets = assets.markets("res/listings.csv")

        eravate = entities.system(name="Eravate")

        opt = { "ly": 50 }

        systems = {}
        for system in galaxy.proximity(system=eravate, options=opt):
            systems[ system["id"] ] = system
        self.assertEqual(len(systems), 519)

        stations = {}
        for station in galaxy.hubs(system=eravate, options=opt):
            stations[ station["id"] ] = station
        self.assertEqual(len(stations), 2081)

        markets = {}
        for station in stations.values():
            markets[ station["id"] ] = entities.market(station["id"])
        self.assertEqual(len(markets), 2081)

        assets.doPickle(systems, "res/systems-mini-50.pic")
        assets.doPickle(stations, "res/stations-mini-50.pic")
        assets.doPickle(markets, "res/markets-mini-50.pic")

if __name__ == "__main__":
    unittest.main()