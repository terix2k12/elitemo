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
        expected = '[{"data": 4615, "value": "Eravate", "label": "Eravate (Linenger\'s Inheritance,Russell Ring,McMahon Dock,Ackerman Market,Maine Hub,Toll Holdings,Cleve Hub,Sylvester City,Scott Prospect,Tiptree Gateway,Bradshaw Vision)"}]'
        self.assertEqual(expected, response)

    def test_autocomplete_systems_broad(self):
        query = "term=Er"
        response = server.handleSystemQuery(query)
        expected = '[{"data": 99, "value": "Eridiani", "label": "Eridiani ()"}, {"data": 4615, "value": "Eravate", "label": "Eravate (Linenger\'s Inheritance,Russell Ring,McMahon Dock,Ackerman Market,Maine Hub,Toll Holdings,Cleve Hub,Sylvester City,Scott Prospect,Tiptree Gateway,Bradshaw Vision)"}]'
        self.assertEqual(expected, response)


    def test_autocomplete_stations(self):
        query = "term=Sylves"
        response = server.handleStationQuery(query)
        expected = '[{"systemId": 4615, "systemName": "Eravate", "data": 232, "value": "Sylvester City", "label": "Sylvester City (Eravate)"}]'
        self.assertEqual(expected, response)

    def test_autocomplete_stations_broad(self):
        query = "term=eng"
        response = server.handleStationQuery(query)
        expected = '[{"systemId": 4615, "systemName": "Eravate", "data": 47747, "value": "Linenger\'s Inheritance", "label": "Linenger\'s Inheritance (Eravate)"}, {"systemId": 4857, "systemName": "Frigaha", "data": 406, "value": "Engle Orbital", "label": "Engle Orbital (Frigaha)"}]'
        self.assertEqual(expected, response)

    def test_autocomplete_stations_withSys(self):
        query = "term=ma&system=4615"
        response = server.handleStationQuery(query)
        self.assertEqual(3, len(json.loads(response)))

    def test_autocomplete_stations_withEmptySys(self):
        query = "term=&system="
        response = server.handleStationQuery(query)
        self.assertEqual(20, len(json.loads(response)))

    def test_autocomplete_stations_withWrongSys(self):
        query = "term=Sylv&system=Nixda"
        response = server.handleStationQuery(query)
        expected = '[{"systemId": 4615, "systemName": "Eravate", "data": 232, "value": "Sylvester City", "label": "Sylvester City (Eravate)"}]'
        self.assertEqual(expected, response)


    def test_autocomplete_commodity(self):
        query = "term=Clothing"
        response = server.handleCommodityQuery(query)
        self.assertEqual('[{"data": 232, "value": "Sylvester City"}]', response)

    def test_autocomplete_commodity(self):
        query = "term=l weapo"
        response = server.handleCommodityQuery(query)
        self.assertEqual('[{"data": 78, "value": "Non-lethal Weapons", "label": "Non-lethal Weapons (Weapons)"}, {"data": 79, "value": "Personal Weapons", "label": "Personal Weapons (Weapons)"}]', response)

    def test_compute(self):
        missioninput = []
        options = {"cargospace" : 16}
        currentStationId = 42180
        missioninput.append( { "source":1, "target":5, "commodity":3, "amount":8, "reward":23000, 'type':'deliver' } )

        inputData = {}
        inputData["options"] = options
        inputData["stationId"] = currentStationId
        inputData["missions"] = missioninput

        server.handleCompute(inputData)

if __name__ == "__main__":
    unittest.main()