import assets
import galaxy
import entities

def getdeals(market1, market2):
	profits = []
	for item1 in market1:
		i1Id = item1["commodity_id"]
		buyPrice = int(item1["buy_price"])
		supply = int(item1["supply"])
		if(supply > 0):
			sellPrice = 0
			for item2 in market2:
				if(item2["commodity_id"] == i1Id):
					sellPrice = int(item2["sell_price"])
					diff =  sellPrice - buyPrice
					if(diff > 0): 
						profits.append((i1Id, diff, supply))
	profits.sort(key=lambda (i,t,p):t, reverse=True)
	return profits 

def compute(options, gcargohold, missiongoals):
    currentStationId = int(options["currentStationId"])

    steps = []

    # pseudocode
    # create node set from galaxy
    # kreuzprodukt aus graph
    #   applz mg auf nodeset
    #    sort nodeset 
    #   schiff laden
    #   yiel auswaehlen (hihgest profi of cargohold)
    #   schiff ausladen
    #   mg aktualisieren
    # 

    missionnodeset = [] # holds tuples of (source, target, profit, modifier, commodity, supply)
    cargohold = [] # holds tuples of (source, target, commodity, loading)
    maxcargospace = int(gcargohold["cargospace"])
    cargospace = maxcargospace # compute gcargohold["emptycargospace"]

    if "ly" not in options:
        options["ly"] = 50

    currentStation = entities.station(id=currentStationId)
    allNeighbors = galaxy.hubs(station=currentStation, options=options)

    failsafe = 0
    while  failsafe < 5:
        failsafe += 1
        instructions = []

        # Unload cargohold
        clone = []
        newinstructions = []
        dropped = {}
        for cargo in cargohold:
            (cargoTarget, cargoCommodityId, cargoVolume) = cargo
            if cargoTarget == currentStationId:
                instructions.append( ('drop',cargo) )
                newinstructions.append( (cargoTarget, cargoCommodityId) )
                if cargoCommodityId not in dropped:
                    dropped[cargoCommodityId] = 0
                dropped[cargoCommodityId] += cargoVolume
                cargospace += cargoVolume
            else:
                clone.append(cargo)
        cargohold = clone

        # Update mission goals
        clone = []
        for mission in missiongoals:
            (missionSource, missionTarget, missionCommodityId, missionVolume, missionReward, missionType) = mission
            if missionCommodityId in dropped:
                droppedAmount = dropped[missionCommodityId]
                if droppedAmount < missionVolume:
                    clone.append( (missionSource, missionTarget, missionCommodityId, missionVolume-droppedAmount, missionReward, missionType) )
            else:
                clone.append(mission)
        missiongoals = clone

        if len(missiongoals) == 0:
            steps.append( (currentStationId, instructions) )
            return steps

        nodeset = []

        # Only use neighbors with a missiongoal
        clone = []

        for neighbor in allNeighbors:
            neighborId = int(neighbor["id"])
            for missiongoal in missiongoals:
                (missionSource, missionTarget, missionCommodityId, missionAmount, missionReward, missionType) = missiongoal
                # TODO other missiontypes
                if missionType in ["Source"]:
                    market2 = entities.market(neighborId)
                    for item in market2:
                        commodityId = int(item["commodity_id"])
                        supply = int(item["supply"])
                        if supply > 0 and missionCommodityId == commodityId:
                            clone.append(neighbor)
                            nodeset.append( (neighborId, missionTarget, missionReward, 0, int(commodityId), missionAmount) )
        neighbors = clone

        # Apply deals
        currentStation = entities.station(id=currentStationId)
        market1 = entities.market(currentStationId)
        for neighbor in neighbors:
            neighborId = int(neighbor["id"])
            market2 = entities.market(neighborId)
            deals = getdeals(market1, market2)
            for deal in deals:
                (commodityId, profit, supply) = deal
                nodeset.append( (currentStationId, neighborId, profit, 0, int(commodityId), supply) )
                
        # TODO mission commodity is missing in deals......

        # Apply missiongoals modifier to nodeset
        clone = []
        for node in nodeset:
            (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId, nodeSupply) = node
            for missiongoal in missiongoals:
                (missionSource, missionTarget, missionCommodityId, missionVolume, missionReward, missionType) = missiongoal
                # if missionType in ['Deliver', 'Intel'] and missionTarget == nodeSource:
                #    nodeModifier = 10000
                #    break
                if missionType in ["Source"] and missionCommodityId == nodeCommodityId and nodeTarget == missionTarget:
                    nodeModifier = 10000
                    break
            clone.append( (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId, nodeSupply) )
        nodeset = clone

        # Select next target
        if len(nodeset) > 0:
            nodeset.sort(key=lambda (s, t, profit, modifier, c, a): (profit+modifier+ (100000 if s == currentStationId else 0) ), reverse=True)
            (s, targetStationId, r, d, c, a) = nodeset[0]
        elif len(cargohold) > 0:
            (newTarget, c, a) = cargohold[0]
            targetStationId = newTarget
        else:
            targetStationId = 0

        if len(missiongoals) > 0:
            # Load cargohold
            clone = []
            for node in nodeset:
                (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId, nodeSupply) = node

                if nodeSource != currentStationId or cargospace == 0:
                    clone.append(node)
                    continue

                if nodeSupply >= cargospace:
                    loading = cargospace
                else:
                    loading = nodeSupply

                transfer = (nodeTarget, nodeCommodityId, loading)

                cargohold.append( transfer )
                cargospace -= loading

                instructions.append( ('collect',transfer) )

                if nodeSupply-loading > 0:
                    clone.append( (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId,  nodeSupply-loading) )
            nodeset = clone

        # Continue the journey
        steps.append( (currentStationId, instructions) )
        currentStationId = targetStationId

        if currentStationId == 0:
            break

    return steps