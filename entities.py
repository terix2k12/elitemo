systemsByName = None
stationsByName = None
stationsBySystemId = None

def systemId(name):
    global systemsByName
    if not systemsByName:
        systemsByName = {}
        for sys in systems.values():
            systemsByName[sys["name"]] = sys["id"]
    if name in systemsByName:
        return systemsByName[name]
    return 0

def system(name=None, id=None, station=None):
    if station:
        id = station["system_id"]
    if name:
        id = systemId(name)
    if id:
        id = int(id)
    if id in systems:
        return systems[int(id)]
    return { "id":0, "name" : "System " + str(id) + "/" + str(name) + " not found."}

def stationId(name):
    global stationsByName
    if not stationsByName:
        stationsByName = {}
        for sta in stations.values():
            stationsByName[sta["name"]] = sta["id"]
    if name in stationsByName:
        return stationsByName[name]
    return 0

def stationsIn(systemId):
    global stationsBySystemId
    if not stationsBySystemId:
        stationsBySystemId = {}
        for station in stations.values():
            sid = station["system_id"]
            if sid not in stationsBySystemId:
                stationsBySystemId[sid] = []
            stationsBySystemId[sid].append(station)
    if systemId in stationsBySystemId:
        return stationsBySystemId[systemId]
    return []

def station(name=None, id=None, system=None, station=None):
    if(station):
        system = entities.systems(station["system_id"])
    if(system): 
        return stationsIn(system["id"])
    if(name):
        id = stationId(name)
    id = int(id)
    if id in stations:
        return stations[id]
    return { "id":0, "name" : "Station " + str(id) + "/" + str(name) + " not found."}

def market(id):
    if(int(id) in markets):
        return markets[int(id)]
    return []

def commodity(market=None, id=None, name=None):
    if(market):
        for item in market:
            if name:
                id = (commodity(name=name))["id"]
            if(int(item["commodity_id"])==int(id)):
                return item
    else:
        for c in commodities:
            if(id):
                if(int(c["id"]) == int(id)):
                    return c
            if(name):
                if(c["name"] == name):
                    return c
    return { "id":id, "name":"Commodity "+ str(id) +"/"+ str(name) +" not found" }

def systemLike(name):
    return nameLike(name, systems.values())

def stationLike(name, system=None):
    if system:
        return nameLike(name, station(system=system))
    else:
        return nameLike(name, stations.values())

def commodityLike(name):
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