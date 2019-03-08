import time
import json
import entities

from urlparse import urlparse
import urllib
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

#// CORS is prohibiting access to external APIs
# // http://localhost:8000/
# // python -m SimpleHTTPServer

HOST_NAME = "localhost" #// "127.0.0.1" 
PORT_NUMBER = 8000

global elite

def handleSystemQuery(query):
	term = query.split("=")[1]
	return ajaxAutocomplete(entities.systemLike(term))

def handleStationQuery(query):
	f = lambda sta: sta["name"] + " (" + entities.system(station=sta)["name"] + ")"
	if query.find("&") > 0:
		term = query.split("&")[0].split("=")[1]
		systemName = (query.split("&")[1].split("=")[1]).replace("+"," ")
		system = entities.system(name=systemName)
		if system["id"] != 0:
			return ajaxAutocomplete(entities.stationLike(term, system=system), [ ("label", f) ])
	else:	
		term = query.split("=")[1]
	return ajaxAutocomplete(entities.stationLike(term), [ ("label", f)])	

def handleCommodityQuery(query):
	term = query.split("=")[1]
	return ajaxAutocomplete(entities.commodityLike(term))	

def ajaxAutocomplete(items, additional=[]):
	response = []
	for item in items:
		dic = { "value" : item[u'name'], "data" : item[u'id'] }
		for (k, f) in additional:
			dic[k] = f(item)
		response.append(dic)
	return json.dumps(response)

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
		global elite
		parse = urlparse(self.path)
		print "Handles GET request: ", parse

		if(parse.path == "/commodities"):
			self.jsonOKHeader()
			response = handleCommodityQuery(parse.query)
			self.wfile.write(response)

		elif(parse.path == "/systems"):
			self.jsonOKHeader()
			response = handleSystemQuery(parse.query)
			self.wfile.write(response)

		elif(parse.path == "/stations"):
			self.jsonOKHeader()
			response = handleStationQuery(parse.query)
			self.wfile.write(response)

		elif(parse.path == "/compute"):
			self.jsonOKHeader()

			term = parse.query.split("=")[1]
			decoded = urllib.unquote(term)

			data = json.loads(decoded)

			data = elite.compute(data)

			self.wfile.write(json.dumps(data))
		else:
			self.send_response(500)
			self.send_header("Content-type", "text/plain")
			self.setCORSHeader()
			self.wfile.write("Access denied.")
			pass



class server:
	def runServer(self):
		print "Starting Server"

		server_class = BaseHTTPServer.HTTPServer
		# handler = MyHandler()
		# handler.setElite(self.elite)
		httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
		print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)

		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			pass

		httpd.server_close()
		print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)