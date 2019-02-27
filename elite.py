from assets import assets
from server import server

class elite:

	def findSystem(name):
		for sys in systems:
			if( sys[u'name'] == name ):
				return sys
	
	def findSystemLike(self, name):
		return self.findNameLike(name, self.systems)
	
	def findStationLike(self, name):
		return self.findNameLike(name, self.stations)
	
	def findCommoditiyLike(self, name):
		return self.findNameLike(name, self.commodities)
	
	def findNameLike(self, name, items):
		result = []
		for item in items: 
			if( self.simple(item[u'name']).find(self.simple(name)) >= 0):
				result.append(item)
		return result
	
	def simple(self, string):
		s = string.upper().replace(" ", "").replace("+","")
		return s 
	
	def distance(self, sys1, sys2):
		a = array( (sys1[u'x'], sys1[u'y'], sys1[u'z']) );
		b = array( (sys2[u'x'], sys2[u'y'], sys2[u'z']) );
		return linalg.norm(a-b);

	def compute(self, data):
		step1 = {}
		step1[u'systemId'] = u'LHS 3447'
		step1["stationId"] = "Bluford Orbital"
		data[u'route'].append(step1)

		print data
		return data

if __name__ == "__main__":
	print "Start Elite:Dangerous Mission Optimizer"

	elite = elite()

	(elite.commodities, elite.systems, elite.stations) = assets().loadAssets()

	server(elite).runServer()

	print "End Elite:D-MO"

#	sid = 0
#
#	eravate = findSystem("Eravate")
#	lhs = findSystem("LHS 3447")
#
#	print findSystemLike("rava")
#
#	sid = eravate[u'id']
#
#	for sta in stations:
#		if( sta[u'system_id'] == sid):
#			print "\t", sta[u'name'], sta[u'id']
#
#	for sys in systems:
#		if( distance(sys, eravate) < 10):
#			print sys[u'name']
#
#	print "Done"