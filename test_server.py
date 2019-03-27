import unittest

import json

import assets
import entities
import server

class TestServer(unittest.TestCase):

    def setUp(self):
        entities.reset()
        entities.markets = assets.markets("test/test-markets.csv")
        entities.systems = assets.systems("test/test-systems.json")
        entities.stations = assets.stations("test/test-stations.json")
        entities.commodities = assets.commodities("res/commodities.json")

    def test_autocomplete_missions(self):
        query = "term=In"
        response = server.handleMissionQuery(query)
        self.assertEqual('[{"data": 1, "value": "Intel"}]', response)

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
        self.assertEqual('[{"data": 232, "value": "Sylvester City", "label": "Sylvester City (Eravate)"}]', response)

    def test_autocomplete_stations_broad(self):
        query = "term=eng"
        response = server.handleStationQuery(query)
        self.assertEqual('[{"data": 47747, "value": "Linenger\'s Inheritance", "label": "Linenger\'s Inheritance (Eravate)"}, {"data": 406, "value": "Engle Orbital", "label": "Engle Orbital (Frigaha)"}]', response)

    def test_autocomplete_stations_withSys(self):
        query = "term=ma&system=Eravate"
        response = server.handleStationQuery(query)
        self.assertEqual(3, len(json.loads(response)))

    def test_autocomplete_stations_withEmptySys(self):
        query = "term=&system="
        response = server.handleStationQuery(query)
        self.assertEqual(20, len(json.loads(response)))

    def test_autocomplete_stations_withWrongSys(self):
        query = "term=Sylv&system=Nixda"
        response = server.handleStationQuery(query)
        self.assertEqual('[{"data": 232, "value": "Sylvester City", "label": "Sylvester City (Eravate)"}]', response)


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