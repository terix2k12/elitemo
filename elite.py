import datetime
import sys

import assets

import galaxy
import entities

from server import server

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

if __name__ == "__main__":
	print "Start Elite:Dangerous Mission Optimizer"

	if len(sys.argv) == 1 and sys.argv[1] == "--update":
		assets.update("res/commodities.json", True)
		assets.update("res/stations.json")
		assets.update("res/systems_populated.json")
		assets.update("res/listings.csv")

	if len(sys.argv) == 1 or sys.argv[1] != "--maxi":
		print "Limited Edition"
		entities.systems = assets.unPickle("res/systems-mini-50.pic")
		entities.stations = assets.unPickle("res/stations-mini-50.pic")
		entities.markets = assets.unPickle("res/markets-mini-50.pic")
	else:
		entities.stations = assets.stations("stations.json")
		entities.systems = assets.systems("systems_populated.json")
		entities.markets = assets.markets("listings.csv")
	
	entities.commodities = assets.commodities("res/commodities.json") 

	server().runServer()

	print "End Elite:D-MO"