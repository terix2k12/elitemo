import unittest

from elite import elite
from assets import assets

class MyTestSuite(unittest.TestCase):

	def test_simplecompute(self):
			
		data = {}
		data['cargohold'] = 288
		data['landingpad'] = "L"
		data['jumprange'] = 13
		data['maxhops'] = 5
	
		step0 = {}
		step0[u'systemId'] = u'LHS 3447'
		step0["stationId"] = "Bluford Orbital"
		data[u'route'] = []
		data[u'route'].append(step0)
	
		result = elite.compute(data)
	
		self.assertEqual(len(result[u'route']), 2)
	
		pass

if __name__ == "__main__":
	elite = elite()

	# (elite.commodities, elite.systems, elite.stations) = assets().loadAssets()

	unittest.main()