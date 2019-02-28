import json
import csv
import elite

class assets:

	def loadJSON(self, name, path):
		print "Loading " +name+ ":"
		f = open(path,"r")
		j = json.load(f)
		print str(len(j)) + " " + name + " parsed"
		f.close()
		return j

	def loadCSV(self, path):
		print "Loading " + path
		f = open(path, "r")
		content = []
		csvrows = csv.DictReader(f, delimiter=",")
		for row in csvrows:
			content.append(row)
		print str(len(content)) + " parsed"
		return content

	def commodities(self):
		return self.loadJSON("commodities","commodities.json")

	def loadSystems(self):
		return self.loadJSON("systems","systems_populated.json")

	def loadStations(self):
		return self.loadJSON("stations","stations.json")

	def markets(self):
		items = self.loadCSV("mini-listings.csv")
		markets = []
		for item in items:
			marketId = int(item["station_id"])
			market = None
			for m in markets:
				if(m.id == marketId):
					market = m
					break
			if not market:
				market = elite.market(marketId)
				markets.append(market)
			market.items.append(item) 
		return markets

	def loadAssets(self):
		print "Loading assets: "
		return (self.loadCommodities(), self.loadSystems(), self.loadStations())

