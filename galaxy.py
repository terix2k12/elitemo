import entities
from numpy import linalg, array

def systems(system=None, station=None, options={}):
    if("ly" in options):
        ly = options["ly"]
        proximity = []
        for sys in entities.systems:
            if(ly > abs(distance(sys, system))):
                proximity.append(sys)
        return proximity
    return []

def stations(system=None, station=None, options={}):
	proxies = []
	for sys in systems(system=system, station=station, options=options):
		for station in entities.station(system=sys):
			proxies.append(station)
	return proxies

def distance(sys1, sys2):
	a = array( (sys1[u'x'], sys1[u'y'], sys1[u'z']) )
	b = array( (sys2[u'x'], sys2[u'y'], sys2[u'z']) )
	return linalg.norm(a-b)