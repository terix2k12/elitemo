import assets
import galaxy
import entities
import elite

def compute(currentStationId, missiongoals, options):
    instructions = []

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
    cargohold = []
    maxcargospace = options["cargo"]
    cargospace = maxcargospace

    currentStation = entities.station(id=currentStationId)
    neighbors = galaxy.hubs(station=currentStation)

    for neighbor in neighbors:
        market1 = entities.market(currentStationId)
        market2 = entities.market(neighbor["id"])
        deals = elite.deals(market1, market2)

        for deal in deals:
            (commodityId, profit, supply) = deal
            nodeset.append( (currentStationId, neighbor["id"], profit, 0, commodityId, supply) )

    while len(missiongoals) > 0:

        # Reset modifiers
        for node in nodeset:
            (source, target, profit, modifier, commodity, supply) = node
            node = (source, target, profit, 0, commodity, supply)

        # Apply missiongoals modifier to nodeset
        for missiongoal in missiongoals:
            (source, target, commodity, amount, reward, missiontype) = missiongoal
            if missiontype in ['deliver', 'intel']:
                nodeset.append( (source, target, reward, 10000, commodity, amount) )

        # Sorting
        nodeset.sort(key=lambda (s, t, profit, d, c, a): profit, reverse=True)

        # Select target
        (s, targetStation, r, d, c, a) = nodeset[0]

        newinstructions = []

        # Load cargohold
        completed = []
        for node in nodeset:
            (source, target, profit, modifier, commodity, supply) = node

            if source != currentStationId:
                break

            if supply >= cargospace:
                loading = cargospace
            else:
                loading = supply

            transfer = (source, target, commodity, loading)

            cargohold.append( transfer )
            cargospace -= loading

            newinstructions.append( transfer )

            if supply-loading == 0:
                completed.append(node)
            else:
                node = (source, target, profit, modifier, commodity, supply-loading)

            if cargospace == 0:
                break

        for i in completed:
            nodeset.remove(i)

        for i in newinstructions:
            instructions.append( i )

        # Update mission goals
        missiongoals = []

    return instructions