import json
import csv

class assets:

	def loadJSON(self, name, path):
		print "Loading " +name+ ":"
		f = open(path,"r")
		j = json.load(f)
		print str(len(j)) + " " + name + " parsed"
		f.close()
		return j

	def loadCSV(self, path):
		f = open(path, "r")
		content = []
		csvrows = csv.DictReader(f, delimiter=",")
		for row in csvrows:
			content.append(row)
		return content

	def loadCommodities(self):
		return self.loadJSON("commodities","commodities.json")

	def loadSystems(self):
		return self.loadJSON("systems","systems_populated.json")

	def loadStations(self):
		return self.loadJSON("stations","stations.json")

	def loadMarkets(self):
		return self.loadCSV("mini-listings.csv")

	def loadAssets(self):
		print "Loading assets: "
		return (self.loadCommodities(), self.loadSystems(), self.loadStations())

