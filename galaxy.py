import entities
from numpy import linalg, array

def proximity(system=None, station=None, options={}):
    if station:
        system = entities.system(station=station)
    proximity = []
    for sys in entities.systems.values():
        if "ly" in options:
            if int(options["ly"]) <= distance(sys, system):
                continue
        proximity.append(sys)
    return proximity

def hubs(system=None, station=None, options={}):
    if station:
        system = entities.system(station=station)
    proxies = []
    for sys in proximity(system=system, station=station, options=options):
        for station in entities.station(system=sys):
            if "landingpad" in options:
                if padsize(options["landingpad"]) > padsize(station["max_landing_pad_size"]):
                    continue
            if "hasCommodity" in options:
                isPresent = False
                for (commodityId, amount) in options["hasCommodity"]:
                    market = entities.market(station["id"])
                    for item in market:
                        if int(item["supply"]) >= amount and commodityId == int(item["commodity_id"]):
                            isPresent = True
                if not isPresent:
                    continue
            proxies.append(station)
    return proxies

def padsize(pad):
    if pad=="None":
        return 4
    if pad=="L":
        return 3
    if pad=="M":
        return 2
    return 1

def distance(sys1, sys2):
    a = array( (sys1[u'x'], sys1[u'y'], sys1[u'z']) )
    b = array( (sys2[u'x'], sys2[u'y'], sys2[u'z']) )
    d = linalg.norm(a-b)
    return abs(d)