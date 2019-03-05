import assets
from server import server

import entities
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

	def sortMarket(self, market, option):
		market.sort(key=lambda i: int(i[option]), reverse=True)

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
		market1 = entities.market(marketId)
		for target in proximity:
			market2 = entities.market(target)
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
		(t, c1, p, s) = deals[0]
		mission = {}
		mission["type"] = "Buy"
		mission["amount"] = s
		mission["commodity"] = self.commodity(id=c)["name"] 
		missions.append(mission)

		step1 = {}
		(t, c2, p, s) = deals[1]
		targetStation = self.station(id=t)
		targetSystem = self.system(id=targetStation["system_id"])
		step1["system"] = targetSystem["name"]
		step1["station"] = targetStation["name"]
		step1["missions"] = []
		mission11 = {}
		mission11["type"] = "Sell"
		mission11["amount"] = s
		mission11["commodity"] = self.commodity(id=c1)["name"]			
		mission12 = {}
		mission12["type"] = "Buy"
		mission12["amount"] = s
		mission12["commodity"] = self.commodity(id=c2)["name"]

		step1["missions"].append(mission11)
		step1["missions"].append(mission12)

		data[u'route'].append(step1)

		mission2 = {}
		mission2["type"] = "Sell"
		mission2["amount"] = s
		mission2["commodity"] = self.commodity(id=c2)["name"]

		(t, c, p, s) = deals[0]
		step2 = {}
		targetStation = self.station(id=t)
		targetSystem = self.system(id=targetStation["system_id"])
		step2["system"] = targetSystem["name"]
		step2["station"] = targetStation["name"]
		step2["missions"] = []

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