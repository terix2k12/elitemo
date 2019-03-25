import assets
import galaxy
import entities

def compute(currentStation, missiongoals, options):
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

    while len(missiongoals) > 0:

        # Reset modifiers
        for node in nodeset:
            (source, target, profit, modifier, commodity, supply) = node
            node = (source, target, profit, 0, commodity, supply)

        # Apply missiongoals modifier to nodeset
        for missiongoal in missiongoals:
            (source, target, commodity, amount, reward, missiontype) = missiongoal
            if missiontype == 'deliver':
                nodeset.append( (source, target, reward, 10000, commodity, amount) )

        # nodeset.sort(key=lambda i: int(i[option]), reverse=True)

        # Select target
        (s, targetStation, r, d, c, a) = nodeset[0]

        newinstructions = []

        # Load cargohold
        for node in nodeset:
            (source, target, profit, modifier, commodity, supply) = node

            if source != currentStation:
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
                nodeset.remove(node)
            else:
                node = (source, target, profit, modifier, commodity, supply-loading)

            if cargospace == 0:
                break

        for i in newinstructions:
            instructions.append( i )

        # Update mission goals
        missiongoals = []

    return instructions