from numpy import linalg, array

def system(name=None, id=None):
	for sys in systems:
		# print sys["id"]
		if( sys[u'name'] == name ) or int(sys[u'id']) == id:
			return sys

def station(name=None, id=None, system=None):
    if(system):
        children = []
        for station in stations:
            if(int(station["system_id"]) == int(system)):
                children.append(station)
        return children
    else:
        for sys in stations:
            if(id):
		        if( int(sys["id"]) == int(id) ):
			        return sys
            else:
		        if( sys["name"] == name):
			        return sys
    return { "id":0, "name" : "Station " + str(id) + "/" + name + " not found."}

def market(id):
	if(int(id) in markets):
		return markets[int(id)]
	return []

def commodity(market=None, id=None, name=None):
    if(market):
        for item in market:
            if(id):
                if(int(item["commodity_id"])==int(id)):
			        return item
#            else:
#                c = commodity(market=None, id=None, name=name)
#                id = c["id"]
#                return commodity(market=market, id=id)
    else:
	    for commodity in commodities:
	    	if(id):
	    		if(int(commodity["id"]) == int(id)):
	    			return commodity
	    	if(name):
	    		if(commodity["name"] == name):
	    			return commodity
    return { "id":id, "name":"Commodity "+ str(id) +"/"+ str(name) +" not found" }

def systemLike(name):
	return nameLike(name, systems)

def stationLike(name):
	return nameLike(name, stations)

def commoditiyLike(name):
	return nameLike(name, commodities)

def nameLike(name, items):
	result = []
	for item in items: 
		if( simple(item[u'name']).find(simple(name)) >= 0):
			result.append(item)
	return result

def simple(string):
	s = string.upper().replace(" ", "").replace("+","")
	return s

def distance(self, sys1, sys2):
	a = array( (sys1[u'x'], sys1[u'y'], sys1[u'z']) )
	b = array( (sys2[u'x'], sys2[u'y'], sys2[u'z']) )
	return linalg.norm(a-b)

def proximity(self, ly, system):
	proximity = []
	for sys in self.systems:
		if(ly > abs(self.distance(sys, system))):
			proximity.append(sys)
	return proximity

# marketIds within distance "ly" of "system"
def proxies(self, ly, system):
	proxies = []
	for sys in self.proximity(ly, system):
		for market in self.children(int(sys["id"])):
			proxies.append(market)
	return proxies