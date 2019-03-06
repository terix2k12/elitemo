import json
import csv

def loadJSON(name, path):
	print "Loading " + name + ":"
	f = open(path,"r")
	j = json.load(f)
	print str(len(j)) + " " + name + " parsed from JSON"
	f.close()
	return j

def loadCSV(path):
	print "Loading " + path + ":"
	f = open(path, "r")
	content = []
	csvrows = csv.DictReader(f, delimiter=",")
	for row in csvrows:
		content.append(row)
	print str(len(content)) + " parsed from CSV"
	return content

def commodities(path):
	return loadJSON("commodities", path)

def systems(path):
	raw = loadJSON("systems", path)
	systems = {}
	for r in raw:
		systems[r["id"]] = r
	return systems

def stations(path):
	raw = loadJSON("stations", path)
	stations = {}
	for r in raw:
		stations[r["id"]] = r
	return stations

def markets(path):
	items = loadCSV(path)
	markets = {}
	for item in items:
		marketId = int(item["station_id"])
		if marketId not in markets:
			markets[marketId] = []
		market = markets[marketId]
		market.append(item) 
	return markets