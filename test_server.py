import unittest

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


if __name__ == "__main__":
    unittest.main()