from assets import assets
from server import server

class market:

	def __init__(self, marketId):
		self.id = marketId
		self.items = []

#	def hasCommodity(self, commoditiyId):
#		return self.marketCommodity(commoditiyId)

	def item(self, commoditiyId):
		for item in self.items:
			if(int(item["commodity_id"]) == commoditiyId):
				return item

	def sortFor(self, option):
		self.items.sort(key=lambda i: int(i[option]), reverse=True)

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

		return data

	def market(self, marketId):
		for market in self.markets:
			if(market.id == marketId):
				return market

	def commodity(self, commoditiyId):
		for commodity in self.commodities:
			if(commodity["id"] == commoditiyId):
				return commodity
		raise Exception("Commodity not found")

	def deals(self, market1, market2):
		profits = []
		for item1 in market1.items:
			c = item1["commodity_id"]
			sellPrice = 0
			for i2 in market2.items:
				if(i2["commodity_id"] == c):
					buyPrice = int(i2["sell_price"]) 

			profits.append((c, int(item1["buy_price"]) - sellPrice))

		profits.sort(key=lambda (i,p) :p, reverse=True)
		return profits 


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