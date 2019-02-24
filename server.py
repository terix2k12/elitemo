import time
import json
from numpy import linalg, array
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

	def do_HEAD(self):
		print "do_HEAD"
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
	def do_GET(self):
		print "Handles GET request:"

		if(self.path == "/commodities"):
			self.send_response(200)
			self.send_header("Content-type", "application/json")
			self.setCORSHeader()
			self.wfile.write(json.dumps(commoditiesJSON))
		else:
			self.send_response(500)
			self.send_header("Content-type", "text/plain")
			self.setCORSHeader()
			self.wfile.write("Access denied.")

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

def distance(sys1, sys2):
	a = array( (sys1[u'x'], sys1[u'y'], sys1[u'z']) );
	b = array( (sys2[u'x'], sys2[u'y'], sys2[u'z']) );
	return linalg.norm(a-b);


if __name__ == "__main__":
	print "Loading assets:"

	#commodities = loadJSON("commodities","commodities.json")
	systems = loadJSON("systems","systems_populated.json")
	stations = loadJSON("stations","stations.json")

	sid = 0

	eravate = findSystem("Eravate")
	lhs = findSystem("LHS 3447")


	sid = eravate[u'id']

	for sta in stations:
		if( sta[u'system_id'] == sid):
			print "\t", sta[u'name'], sta[u'id']

	for sys in systems:
		if( distance(sys, eravate) < 10):
			print sys[u'name']

	print "Done"