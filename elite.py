import datetime

import assets
from server import server
import galaxy
import entities

def time(utc):
	dt = datetime.datetime.fromtimestamp(int(utc))
	return dt.strftime('%Y-%m-%d %H:%M:%S')

def age(utc):
	dt = datetime.datetime.fromtimestamp(int(utc))
	dx = datetime.datetime.now()
	print (dx - dt)
	return 4

def sortMarket(market, option):
	market.sort(key=lambda i: int(i[option]), reverse=True)

def deals(market1, market2):
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

def dealOneTrip(marketId, targetId, cargohold):
	profits = []
	market1 = entities.market(marketId)
	market2 = entities.market(targetId)

	dealsTo = deals(market1, market2)
	ct = p = s = x = e = 0
	instructions = []
	for (ct,p,s) in dealsTo:
		if( x == cargohold):
			break
		if( x+s > cargohold):
			s = cargohold - x
		instructions.append( (marketId,target,ct,p*s,s) )
		x += s
		e += (p * s)

	return instructions

def bestdealOneway(marketId, proximity, cargohold):
	profits = []
	market1 = entities.market(marketId)
	for target in proximity:
		market2 = entities.market(target)
		dealsTo = deals(market1, market2)
		ct = p = s = x = e = 0
		instructions = []
		for (ct,p,s) in dealsTo:
			if( x == cargohold):
				break
			if( x+s > cargohold):
				s = cargohold - x
			instructions.append( (marketId,target,ct,p*s,s) )
			x += s
			e += (p * s)
		profits.append( (e,instructions) )
	profits.sort(key=lambda (profit,instructions):profit, reverse=True)
	return profits[0]

def bestdealReturn(marketId, proximity, cargohold):
	profits = []
	market1 = entities.market(marketId)
	for target in proximity:
		market2 = entities.market(target)
		dealsTo = deals(market1, market2)
		dealsFrom = deals(market2, market1)
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

def compute(data):
	# Get basic parameters
	cargo = 0
	if "cargohold" in data:
		if data["cargohold"]:
			cargo = int(data["cargohold"])
	ly = 50
	if "jumprange" in data:
		if data["jumprange"]:
			ly = int(data["jumprange"])
	pad = "S"
	if "landingpad" in data:
		if data["landingpad"]:
			pad = data["landingpad"]
	maxstopps = 1
	if "maxstopps" in data:
		if data["maxstopps"]:
			maxstopps = data["maxstopps"]

	opt = { "ly": ly, "cargohold": cargo, "landingpad": pad}

	steps = data["steps"]

	# Easy cases:

	if maxstopps == 1:

		step0 = steps[0]
		system = entities.system(name=step0["system"])
		inst = step0["instructions"] = []

		if "missions" in step0:
			for mission in step0["missions"]:

				if mission["type"] == "Intel":
					station = entities.station(name=step0["station"])
					targetSystem = entities.system(name= mission["system"] )
					targetStation = entities.station(name= mission["station"] )
					reward = mission["reward"]
					
					instructions =  (station["name"], targetStation["name"], 0, reward, 0, 0)
					inst.append( instructions )

					deals = dealOneTrip(station["id"], targetStation["id"], cargo)
					for deal in deals:
						inst.append( deal )

					return data
				
				if mission["type"] == "Delivery":
					station = entities.station(name=step0["station"])
					targetSystem = entities.system(name= mission["system"] )
					targetStation = entities.station(name= mission["station"] )
					reward = mission["reward"]
					commodity = entities.commodity(name=mission["commodity"])
					amount = int(mission["amount"])

					instructions =  (station["name"], targetStation["name"], commodity["id"], reward, 0, amount)
					inst.append( instructions )

					deals = dealOneTrip(station["id"], targetStation["id"], cargo-amount)
					for deal in deals:
						inst.append( deal )

				if mission["type"] == "Source":
					commodity = entities.commodity(name=mission["commodity"])
					sourceCommodityId = int(commodity["id"])
					sourceAmount = int(mission["amount"])
					reward = mission["reward"]
					originStation = entities.station(name=step0["station"])

					opt["commodity"] = [ (sourceCommodityId, sourceAmount) ]
					prox = galaxy.hubs(station=originStation, options=opt) 
					sourceStationId = prox[0]["id"]

					deals = dealOneTrip(originStation["id"], sourceStationId, cargo)
					if len(deals):
						for deal in deals:
							inst.append( deal )
					else:
						instructions =  (originStation["name"], prox[0]["name"], commodity["name"], 0, 0, 0)
						inst.append( instructions )

	return data


#					# TODO choose best proxies out of these
#					# TODO consider return payload too 
#					# proxies = [ p["id"] for p in prox]	
#					# (profit, instructions) = bestdealOneway(station["id"], proxies, cargo)
#					# (marketId,target,ct,cx,s) = instructions
#					inst = step0["instructions"] = []
#					inst.append( (sourceStationId, originStation["id"], sourceCommodityId, reward, sourceAmount) )
#					return data
#
#		# Case 1.1.a : 1 Stopp, no start, no target, no mission
#		if not "station" in step0:
#			prox = galaxy.hubs(system=system, options=opt)
#			proxies = [ p["id"] for p in prox] 
#			trades = []
#			for proxy in proxies:
#				(profit, instructions) = bestdealOneway(proxy, proxies, cargo)
#				trades.append( (profit, instructions) )
#			trades.sort(key=lambda (p,i):p, reverse=True)
#			(profit, instructions) = trades[0]
#		# Case 1.1.b : 1 stopp, start, no target, no mission
#		else:
#			station = entities.station(name=step0["station"])
#			prox = galaxy.hubs(system=system, options=opt)
#			proxies = [ p["id"] for p in prox] 
#			(profit, instructions) = bestdealOneway(station["id"], proxies, cargo)
#		
#		if not profit:
#			return data
#		inst = step0["instructions"] = []
#		inst.append( instructions )
#		return data

		# Case 1.2 : 1 Jump, explicit commodity

		# Case 1.3 : "deliver" 1 Jump, explicit target

	# Case 2 - max 2 stopps


#	for step in steps:
#		if maxjumps <= len(steps)-1:
#			break
#
#		if step["complete"]:
#			continue
#		
#		if not len(step["missions"]):
#
#			if not gross:
#				step["complete"] = 1
#				continue
#
#			missions = step["missions"] = []
#			(t, c1, p, s) = deals[0]
#			mission = {}
#			mission["type"] = "Buy"
#			mission["amount"] = s
#			mission["commodity"] = entities.commodity(id=c1)["name"] 
#			missions.append(mission)
#
#			step1 = {}
#			(t, c2, p, s) = deals[1]
#			targetStation = entities.station(id=t)
#			targetSystem = entities.system(id=targetStation["system_id"])
#			step1["system"] = targetSystem["name"]
#			step1["station"] = targetStation["name"]
#			step1["missions"] = []
#			mission11 = {}
#			mission11["type"] = "Sell"
#			mission11["amount"] = s
#			mission11["commodity"] = entities.commodity(id=c1)["name"]			
#			step1["missions"].append(mission11)
#			step1["complete"] = 1	
#
#			data[u'route'].append(step1)
#	return data


if __name__ == "__main__":
	print "Start Elite:Dangerous Mission Optimizer"

	entities.stations = assets.stations("stations.json")
	entities.systems = assets.systems("systems_populated.json")
	entities.markets = assets.markets("listings.csv")
	entities.commodities = assets.commodities("commodities.json") 

	server().runServer()

	print "End Elite:D-MO"