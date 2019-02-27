from elite import elite
from assets import assets

def test_simplecompute():
		
	data = {}
	data.cargohold = 288
	data.landingpad = "L"
	data.jumprange = 13
	data.maxhops = 5

	step0 = {}
	step0[u'systemId'] = u'LHS 3447'
	step0["stationId"] = "Bluford Orbital"
	data[u'route'].append(step0)

	result = elite.compute(data)

	assert(len(result[u'route']), 2)

	pass

if __name__ == "__main__":
	print "Start Tests"

	elite = elite()

	(elite.commodities, elite.systems, elite.stations) = assets().loadAssets()

	

	print "End Elite:D-MO"