import unittest
import assets
import entities
import elitecore

class TestCore(unittest.TestCase):

    def setUp(self):
        entities.reset()
        entities.markets = assets.markets("test/test-markets.csv")
        entities.systems = assets.systems("test/test-systems.json")
        entities.stations = assets.stations("test/test-stations.json")
        entities.commodities = assets.commodities("res/commodities.json")

    def test_core_deliver(self):
        missioninput = []
        
        # Deliver
        currentStation = 1
        missioninput.append( (1, 5, 3) ) 
        
        elitecore.compute(currentStation, missioninput)

        self.assertEqual(3, 3)

if __name__ == "__main__":
	unittest.main()