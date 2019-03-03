import assets
from server import server
from numpy import linalg, array
import datetime

class elite:

	def time(self, utc):
		dt = datetime.datetime.fromtimestamp(int(utc))
		return dt.strftime('%Y-%m-%d %H:%M:%S')

	def age(self, utc):
		dt = datetime.datetime.fromtimestamp(int(utc))
		dx = datetime.datetime.now()
		print (dx - dt)
		return 4

	def system(self, name=None, id=None):
		for sys in self.systems:
			# print sys["id"]
			if( sys[u'name'] == name ) or int(sys[u'id']) == id:
				return sys

	def station(self, name=None, id=None):
		for sys in self.stations:
			# print sys["id"]
			if( sys[u'name'] == name ) or int(sys[u'id']) == id:
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

	def proximity(self, ly, system):
		proximity = []
		for sys in self.systems:
			if(ly > abs(self.distance(sys, system))):
				proximity.append(sys)
		return proximity

	def market(self, marketId):
		if( marketId in self.markets):
			return self.markets[marketId]
		return []

	def children(self, systemId):
		children = []
		for station in self.stations:
			if(int(station["system_id"]) == systemId):
				children.append(int(station["id"]))
		return children

	# marketIds within distance "ly" of "system"
	def proxies(self, ly, system):
		proxies = []
		for sys in self.proximity(ly, system):
			for market in self.children(int(sys["id"])):
				proxies.append(market)
		return proxies

	def item(self, market, commoditiyId):
		for item in market:
			if(int(item["commodity_id"])==commoditiyId):
				return item

	def sortMarket(self, market, option):
		market.sort(key=lambda i: int(i[option]), reverse=True)

	def commodity(self, commoditiyId):
		for commodity in self.commodities:
			if(commodity["id"] == commoditiyId):
				return commodity
		raise Exception("Commodity not found")

	def deals(self, market1, market2):
		profits = []
		for item1 in market1:
			i1Id = item1["commodity_id"]
			buyPrice = int(item1["buy_price"])
			supply = int(item1["supply"])
			if(supply > 0):
				sellPrice = 0
				for item2 in market2:
					if(item2["commodity_id"] == i1Id):
						sellPrice = int(item2["sell_price"])
						diff =  sellPrice - buyPrice
						if(diff > 0): 
							profits.append((i1Id, diff, supply))

		profits.sort(key=lambda (i,t,p):t, reverse=True)
		return profits 

	def bestdeals(self, marketId, proximity, cargohold):
		profits = []
		market1 = self.market(marketId)
		for target in proximity:
			market2 = self.market(target)
			dealsTo = self.deals(market1, market2)
			dealsFrom = self.deals(market2, market1)
			ct = cf = q = p = s = r = e = x = z = 0
			instructions = []
			for (ct,p,s) in dealsTo:
				if( x == cargohold):
					break
				if( x+s > cargohold):
					s = cargohold - x
				instructions.append( (marketId,ct,p,s) )
				x += s
				e += (p * s)
			if not len(dealsTo):
				instructions.append( (marketId, 0,0,0) )
 			for (cf,q,r) in dealsFrom:
				if( z == cargohold):
					break
				if( z+r > cargohold):
					r = cargohold - z
				instructions.append( (target,cf,q,r) )
				z += r
				e += (q * r)
			profits.append( (e,instructions) )
			if not len(dealsFrom):
				instructions.append( (target, 0,0,0) )

		profits.sort(key=lambda (profit,instructions):profit, reverse=True)
		return profits[0]

	def compute(self, data):
		stationName = data["route"][0]["stationId"]

		station = self.findStationLike(stationName)[0]
		marketId = station["id"]
		system = self.system(id=station["system_id"])

		proxies = self.proxies(15, system)

		(gross, deals) = self.bestdeals(marketId, proxies, 200)

		step0 = data["route"][0]
		missions = step0["missions"] = []
		(t, c, p, s) = deals[0]
		mission = {}
		mission["type"] = "pickup"
		mission["amount"] = s
		mission["commodity"] = c 
		missions.append(mission)

		step1 = {}
		targetStation = self.station(id=t)
		targetSystem = self.system(id=targetStation["system_id"])
		step1["systemId"] = targetSystem["name"]
		step1["stationId"] = targetStation["name"]
		step1["missions"] = []
		mission11 = {}
		mission11["type"] = "drop"
		mission11["amount"] = s
		mission11["commodity"] = c		
		
		(t, c, p, s) = deals[1]
		mission12 = {}
		mission12["type"] = "pickup"
		mission12["amount"] = s
		mission12["commodity"] = c

		step1["missions"].append(mission11)
		step1["missions"].append(mission12)

		data[u'route'].append(step1)
		
		step2 = {}
		targetStation = self.station(id=t)
		targetSystem = self.system(id=targetStation["system_id"])
		step2["systemId"] = targetSystem["name"]
		step2["stationId"] = targetStation["name"]
		step2["missions"] = []
		mission2 = {}
		mission2["type"] = "drop"
		mission2["amount"] = s
		mission2["commodity"] = c
		step2["missions"].append(mission2)	
		
		data[u'route'].append(step2)

		return data

if __name__ == "__main__":
	print "Start Elite:Dangerous Mission Optimizer"

	elite = elite()

	elite.stations = assets.stations("stations.json")
	elite.systems = assets.systems("systems_populated.json")
	elite.markets = assets.markets("listings.csv")
	elite.commodities = assets.commodities("commodities.json") 

	server(elite).runServer()

	print "End Elite:D-MO"