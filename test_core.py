import unittest
import assets
import entities
import elitecore

class TestCore(unittest.TestCase):

    def setUp(self):
        entities.reset()
        entities.markets = assets.markets("test/test-markets3.csv")
        entities.systems = assets.systems("test/test-systems2.json")
        entities.stations = assets.stations("test/test-stations2.json")
        entities.commodities = assets.commodities("res/commodities.json")

    def xy_test_core_deliver(self):
        missioninput = []
        options = {"cargospace" : 16}
        
        # Deliver
        currentStation = 1
        missioninput.append( (1, 5, 3, 8, 23000, 'deliver') )
        
        instructions = elitecore.compute(currentStation, missioninput, options)

        self.assertEqual( len(instructions) , 1)
        self.assertEqual( instructions, [(1, 5, 3, 8)] )

    def _test_core_intel(self):
        missioninput = []
        options = {"cargospace" : 16}

        # Intel
        currentStation = 5
        missioninput.append( (5, 1, 0, 0, 23000, 'intel') )

        instructions = elitecore.compute(currentStation, missioninput, options)

        self.assertEqual( len(instructions) , 2)
        self.assertEqual( instructions, [(5, 1, 0, 0), (5, 1, '10', 10)] )

    def test_core_source(self):
        currentStationId = 5
        options = {"ly":1000, "currentStationId":currentStationId }
        cargohold = {"cargospace" : 16}
        missiongoals = []
        missiongoals.append( (0, 5, 1, 10, 23000, 'Source') )

        instructions = elitecore.compute(options, cargohold, missiongoals)

        self.assertEqual( len(instructions) , 3)
        self.assertEqual( instructions, [
            (5,
                [('collect', (1, 2, 10))]
            ),
            
            (1,
                [('drop', (1, 2, 10)), ('collect', (5, 1, 10)), ('collect', (5, 3, 6))]
            ),
            
            (5,
                [('drop', (5, 1, 10)), ('drop', (5, 3, 6))]
            )
        ])

if __name__ == "__main__":
	unittest.main()