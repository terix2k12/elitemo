import json
import csv
import cPickle
import wget
import os
import sys

def loadJSON(name, path):
	print "Loading '" + name + "':"
	f = open(path,"r")
	j = json.load(f)
	print str(len(j)) + " " + name + " parsed from JSON"
	f.close()
	return j

def loadJSONl(path, properties):
	print "Loading with line break '" + path + "':"
	mapping = {}
	with open(path) as f:
		for line in f:
			fulljson = json.loads(line)
			smalljson = {}
			for prop in properties:
				smalljson[prop] = fulljson[prop]
			mapping[smalljson["id"]] = smalljson
	print str(len(mapping.keys())) + " parsed from JSONL " + path
	return mapping

def loadCSV(path):
	print "Loading " + path + ":"
	f = open(path, "r")
	content = []
	csvrows = csv.DictReader(f, delimiter=",")
	for row in csvrows:
		content.append(row)
	print str(len(content)) + " parsed from CSV"
	f.close()
	return content

def commodities(path):
	return loadJSON("commodities", path)

def systems_full(path):
	raw = loadJSON("systems", path)
	systems = {}
	for r in raw:
		systems[r["id"]] = r
	return systems

def systems(path):
	properties = ["id", "name", "x","y","z","needs_permit"]
	return loadJSONl(path, properties)

def stations_full(path):
	raw = loadJSON("stations", path)
	stations = {}
	for r in raw:
		stations[r["id"]] = r
	return stations

def stations(path):
	properties = ["id", "name", "system_id", "market_updated_at", "max_landing_pad_size","is_planetary","distance_to_star"]
	return loadJSONl(path, properties)

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

def doPickle(dict, filename): 
	outfile = open(filename,'wb')
	cPickle.dump(dict,outfile)
	outfile.close()

def unPickle(filename):
	infile = open(filename,'rb')
	dict = cPickle.load(infile)
	infile.close()
	print "Unpickled " + str( len(dict) )
	return dict

def update(filename, force=False):
	exists = os.path.isfile(filename)
	if exists:
		if not force:
			print "Resource already present, ignore update for " + filename
			return False
		print "Updating resource " + filename
		os.remove(filename)
	print "Downloading resource " + filename
	try:
		fileurl = filename.split("/")[1]
		url = "https://eddb.io/archive/v6/" + fileurl
		wget.download(url, filename)
		return True
	except Exception:
		return False
	return False

def deepsize(element):
	size = sys.getsizeof(element)
	if type(element) is list:
		for item in element:
			size += deepsize(item)
	if type(element) is dict:
		for key in element.keys():
			size += sys.getsizeof(key)
			size += deepsize(element[key])
	return size