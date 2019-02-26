import time
import json
from numpy import linalg, array
from urlparse import urlparse
import urllib
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

HOST_NAME = "localhost" #// "127.0.0.1" 
PORT_NUMBER = 8000


#// CORS is prohibiting access to external APIs
# // http://localhost:8000/
# // python -m SimpleHTTPServer

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def setCORSHeader(self):
		self.send_header('Access-Control-Allow-Origin', '*')
		self.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
		self.send_header('Access-Control-Allow-Methods', 'GET') # ,PUT,POST,DELETE	 
		self.end_headers()

	def jsonOKHeader(self):
		self.send_response(200)
		self.send_header("Content-type", "application/json")
		self.setCORSHeader()

	def do_POST():
		print "do_POST"

	def do_HEAD(self):
		print "do_HEAD"
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
	def do_GET(self):
		parse = urlparse(self.path)
		print "Handles GET request: ", parse

		if(parse.path == "/commodities"):
			self.jsonOKHeader()
			term = parse.query.split("=")[1]

			self.wfile.write(ajaxAutocomplete(findCommoditiyLike(term)))
		elif(parse.path == "/systems"):
			self.jsonOKHeader()
			term = parse.query.split("=")[1]

			self.wfile.write(ajaxAutocomplete(findSystemLike(term)))
		elif(parse.path == "/stations"):
			self.jsonOKHeader()
			term = parse.query.split("=")[1]

			self.wfile.write(ajaxAutocomplete(findStationLike(term)))
		elif(parse.path == "/compute"):
			self.jsonOKHeader()

			term = parse.query.split("=")[1]
			decoded = urllib.unquote(term)

			data = json.loads(decoded)

			

			self.wfile.write("My answer")
		else:
			self.send_response(500)
			self.send_header("Content-type", "text/plain")
			self.setCORSHeader()
			self.wfile.write("Access denied.")

def ajaxAutocomplete(items):
	response = []
	for item in items:
		dic = { "value" : item[u'name'], "data" : item[u'id'] }
		response.append(dic)
	return json.dumps(response)

def runServer():
	print "Starting Server"

	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)

	try:
			httpd.serve_forever()
	except KeyboardInterrupt:
			pass

	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

def loadJSON(name, path):
	print "Loading " +name+ ":"
	f = open(path,"r")
	j = json.load(f)
	print str(len(j)) + " " + name + " parsed"
	f.close()
	return j

def findSystem(name):
	for sys in systems:
		if( sys[u'name'] == name ):
			return sys

def findSystemLike(name):
	return findNameLike(name, systems)

def findStationLike(name):
	return findNameLike(name, stations)

def findCommoditiyLike(name):
	return findNameLike(name, commodities)

def findNameLike(name, items):
	result = []
	for item in items: 
		if( simple(item[u'name']).find(simple(name)) >= 0):
			result.append(item)
	return result

def simple(string):
	s = string.upper().replace(" ", "").replace("+","")
	return s 

def distance(sys1, sys2):
	a = array( (sys1[u'x'], sys1[u'y'], sys1[u'z']) );
	b = array( (sys2[u'x'], sys2[u'y'], sys2[u'z']) );
	return linalg.norm(a-b);

if __name__ == "__main__":
	print "Loading assets:"

	commodities = loadJSON("commodities","commodities.json")
#	systems = loadJSON("systems","systems_populated.json")
#	stations = loadJSON("stations","stations.json")

	runServer()

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