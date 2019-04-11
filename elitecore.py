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
    neighbors = galaxy.hubs(station=currentStation, options=options)

    clone = []
    market1 = entities.market(currentStationId)
    for neighbor in neighbors:
        neighborId = int(neighbor["id"])
        market2 = entities.market(neighborId)

        # Apply 'source' mission modifiers
        for missiongoal in missiongoals:
            (missionSource, missionTarget, missionCommodityId, missionAmount, missionReward, missionType) = missiongoal
            if missionType in ["Source"]:
                for item in market2:
                    commodityId = int(item["commodity_id"])
                    supply = int(item["supply"])
                    if supply > 0 and missionCommodityId == commodityId:
                        if neighborId==currentStationId:
                            print "Bringt nix"
                        clone.append(neighbor)
                        missionnodeset.append( (neighborId, missionTarget, missionReward, 0, missionCommodityId, supply) )
    neighbors = clone

    failsafe = 0
    while len(missiongoals) > 0 and failsafe < 5:
        failsafe += 1
        instructions = []

        nodeset = []
        for node in missionnodeset:
            nodeset.append(node)

        currentStation = entities.station(id=currentStationId)
        neighbors = galaxy.hubs(station=currentStation, options=options)

        market1 = entities.market(currentStationId)
        for neighbor in neighbors:
            neighborId = int(neighbor["id"])
            market2 = entities.market(neighborId)

            # Apply deals
            deals = getdeals(market1, market2)
            for deal in deals:
                (commodityId, profit, supply) = deal
                nodeset.append( (currentStationId, neighborId, profit, 0, int(commodityId), supply) )        

        # Reset modifiers
        clone = []
        for node in nodeset:
            (source, target, profit, modifier, commodityId, supply) = node
            clone.append( (source, target, profit, 0, commodityId, supply) )
        nodeset = clone

        # Apply missiongoals modifier to nodeset
        clone = []
        for node in nodeset:
            (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId, nodeSupply) = node
            for missiongoal in missiongoals:
                (missionSource, missionTarget, missionCommodityId, missionVolume, missionReward, missionType) = missiongoal
                # if missionType in ['Deliver', 'Intel'] and missionTarget == nodeSource:
                #    nodeModifier = 10000
                #    break
                if missionType in ["Source"] and missionCommodityId == nodeCommodityId:
                    nodeModifier = 10000
                    break
            clone.append( (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId, nodeSupply) )
        nodeset = clone

        # Unload cargohold
        clone = []
        newinstructions = []
        for cargo in cargohold:
            (cargoTarget, cargoCommodityId, cargoVolume) = cargo
            if cargoTarget == currentStationId:
                instructions.append( ('drop',cargo) )
                newinstructions.append(cargo)
                cargospace += cargoVolume
            else:
                clone.append(cargo)
        cargohold = clone

        # Update mission goals
        clone = []
        for mission in missiongoals:
            (missionSource, missionTarget, missionCommodityId, missionVolume, missionReward, missionType) = missiongoal
            node = (missionTarget, missionCommodityId, missionVolume)
            missionCompleted = node in newinstructions
            if not missionCompleted:
                clone.append(mission)
        missiongoals = clone

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