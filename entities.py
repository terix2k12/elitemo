systemsByName = None
stationsByName = None

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
    if(station):
        id = station["system_id"]
    if(name):
        id = systemId(name)
    if id in systems:
        return systems[int(id)]
    return { "id":0, "name" : "System " + str(id) + "/" + name + " not found."}

def stationId(name):
    global stationsByName
    if not stationsByName:
        stationsByName = {}
        for sta in stations.values():
            stationsByName[sta["name"]] = sta["id"]
    if name in stationsByName:
        return stationsByName["name"]
    return 0

# def stationsIn(systemId):
#     children = []
#     for station in stations.values:
#         if( int(station["system_id"]) == int(systemId)):
#             children.append(station)

def station(name=None, id=None, station=None):
    if(station):
        system = entities.systems(station["system_id"])
#    if(system): system=None,
#        return stationsIn(system["id"])
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