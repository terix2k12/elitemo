import assets
import galaxy
import entities
import elite

def compute(currentStationId, missiongoals, options):
    
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

    nodeset = [] # holds tuples of (source, target, profit, modifier, commodity, supply)
    cargohold = [] # holds tuples of (source, target, commodity, loading)
    maxcargospace = options["cargo"]
    cargospace = maxcargospace

    currentStation = entities.station(id=currentStationId)
    neighbors = galaxy.hubs(station=currentStation)

    for neighbor in neighbors:
        neighborId = int(neighbor["id"])
        market1 = entities.market(currentStationId)
        market2 = entities.market(neighborId)

        # Apply deals
        deals = elite.deals(market1, market2)
        for deal in deals:
            (commodityId, profit, supply) = deal
            nodeset.append( (currentStationId, neighborId, profit, 0, int(commodityId), supply) )

        # Apply 'source' mission modifiers
        for missiongoal in missiongoals:
            (missionSource, missionTarget, missionCommodityId, missionAmount, missionReward, missionType) = missiongoal
            if missionType in ['source']:
                for item in market2:
                    commodityId = int(item["commodity_id"])
                    if missionCommodityId == commodityId:
                        nodeset.append( (neighborId, missionTarget, missionReward, 0, missionCommodityId, int(item["supply"])) )

    while len(missiongoals) > 0:
        instructions = []

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
                if missionType in ['deliver', 'intel']:
                    nodeModifier = 10000
                    break
                if missionType in ['source'] and missionCommodityId == nodeCommodityId:
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
            nodeset.sort(key=lambda (s, t, profit, modifier, c, a): (profit+modifier+ (100000000 if s == currentStationId else 0) ), reverse=True)
            (s, targetStationId, r, d, c, a) = nodeset[0]
        elif len(cargohold) > 0:
            (newTarget, c, a) = cargohold[0]
            targetStationId = newTarget
        else:
            targetStationId = 0

        # Load cargohold
        clone = []
        for node in nodeset:
            (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId, nodeSupply) = node

            if nodeSource != currentStationId or cargospace == 0:
                clone.append(node)
                continue

            if supply >= cargospace:
                loading = cargospace
            else:
                loading = supply

            transfer = (nodeTarget, nodeCommodityId, loading)

            cargohold.append( transfer )
            cargospace -= loading

            instructions.append( ('collect',transfer) )

            if supply-loading > 0:
                clone.append( (nodeSource, nodeTarget, nodeProfit, nodeModifier, nodeCommodityId,  supply-loading) )
        nodeset = clone

        # Continue the journey
        steps.append( (currentStationId, instructions) )
        currentStationId = targetStationId

    return steps