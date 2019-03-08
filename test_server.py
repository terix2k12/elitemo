import unittest

import json

import assets
import entities
import server

class TestServer(unittest.TestCase):

    def setUp(self):
        entities.markets = assets.markets("test/test-markets.csv")
        entities.systems = assets.systems("test/test-systems.json")
        entities.stations = assets.stations("test/test-stations.json")
        entities.commodities = assets.commodities("commodities.json")


    def test_autocomplete_systems(self):
        query = "term=Erav"
        response = server.handleSystemQuery(query)
        self.assertEqual('[{"data": 4615, "value": "Eravate"}]', response)

    def test_autocomplete_systems_broad(self):
        query = "term=Er"
        response = server.handleSystemQuery(query)
        self.assertEqual('[{"data": 99, "value": "Eridiani"}, {"data": 4615, "value": "Eravate"}]', response)


    def test_autocomplete_stations(self):
        query = "term=Sylves"
        response = server.handleStationQuery(query)
        self.assertEqual('[{"data": 232, "system": "Eravate", "value": "Sylvester City"}]', response)

    def test_autocomplete_stations_broad(self):
        query = "term=eng"
        response = server.handleStationQuery(query)
        self.assertEqual('[{"data": 47747, "system": "Eravate", "value": "Linenger\'s Inheritance"}, {"data": 406, "system": "Frigaha", "value": "Engle Orbital"}]', response)

    def test_autocomplete_stations_withSys(self):
        query = "term=ma&system=Eravate"
        response = server.handleStationQuery(query)
        self.assertEqual(3, len(json.loads(response)))

    def test_autocomplete_stations_withWrongSys(self):
        query = "term=Sylv&system=Nixda"
        response = server.handleStationQuery(query)
        self.assertEqual('[{"data": 232, "system": "Eravate", "value": "Sylvester City"}]', response)


    def test_autocomplete_commodity(self):
        query = "term=Clothing"
        response = server.handleCommodityQuery(query)
        self.assertEqual('[{"data": 232, "value": "Sylvester City"}]', response)

    def test_autocomplete_commodity(self):
        query = "term=l weapo"
        response = server.handleCommodityQuery(query)
        self.assertEqual('[{"data": 78, "value": "Non-lethal Weapons"}, {"data": 79, "value": "Personal Weapons"}]', response)


if __name__ == "__main__":
    unittest.main()