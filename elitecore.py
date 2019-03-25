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

    nodeset = []
    cargohold = []
    maxcargospace = options["cargo"]
    cargospace = maxcargospace

    while len(missiongoals) > 0:

        # Apply missiongal modifier to nodeset
        for missiongoal in missiongoals:
            (source, target, commodity, amount, reward, missiontype) = missiongoal
            if missiontype == 'deliver':
                nodeset.append( (source, target, reward, 10000, commodity, amount) )

        # nodeset.sort(key=lambda i: int(i[option]), reverse=True)

        # Select target
        (s, target, r, d, c, a) = nodeset[0]

        newinstrucions = []

        # Load cargohold
        for node in nodeset:
            cargohold.append( (currentStation, target, c, a) )
            cargospace -= a

            newinstrucions.append( (currentStation, target, c, a) )

            if cargospace == 0:
                break

        # Update mission goals
        missiongoals = []

    return instructions