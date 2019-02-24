import time
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

HOST_NAME = "localhost" 
#// "127.0.0.1" 
PORT_NUMBER = 8000

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
			self.send_header("Content-type", "text/json")
			self.setCORSHeader()
			self.wfile.write(commoditiesJSON)
		else:
			self.send_response(500)
			self.send_header("Content-type", "text/plain")
			self.setCORSHeader()
			self.wfile.write("Access denied.")

if __name__ == "__main__":
	print "Loading assets:"
	commoditiesJSON = "{ name: 'cheese'}"

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