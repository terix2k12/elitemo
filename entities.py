def nameOrId(entity, id, name):
    if(id):
        return int(entity["id"]) == int(id)
    else:
        return entity["name"] == name

def system(name=None, id=None, station=None):
    if(station):
        id = station["system_id"]
    for sys in systems:
        if( nameOrId(sys, id, name) ):
            return sys
    return { "id":0, "name" : "System " + str(id) + "/" + name + " not found."}

def station(name=None, id=None, system=None, station=None):
    if(station):
        system = entities.systems(station["system_id"])
    if(system):
        id = system["id"]
        children = []
        for station in stations:
            if(int(station["system_id"]) == int(id)):
                children.append(station)
        return children
    else:
        for sta in stations:
            if( nameOrId(sta, id, name) ):
                return sta
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