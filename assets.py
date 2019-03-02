import json
import csv

class assets:

	def loadJSON(self, name, path):
		print "Loading " + name + ":"
		f = open(path,"r")
		j = json.load(f)
		print str(len(j)) + " " + name + " parsed from JSON"
		f.close()
		return j

	def loadCSV(self, path):
		print "Loading " + path + ":"
		f = open(path, "r")
		content = []
		csvrows = csv.DictReader(f, delimiter=",")
		for row in csvrows:
			content.append(row)
		print str(len(content)) + " parsed from CSV"
		return content

	def commodities(self, path):
		return self.loadJSON("commodities", path)

	def systems(self, path):
		return self.loadJSON("systems", path)

	def stations(self, path):
		return self.loadJSON("stations", path)

	def markets(self, path):
		items = self.loadCSV(path)
		markets = {}
		for item in items:
			marketId = int(item["station_id"])
			if marketId not in markets:
				markets[marketId] = []
			market = markets[marketId]
			market.append(item) 
		return markets