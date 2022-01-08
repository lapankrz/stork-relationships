import overpy

api = overpy.Overpass()

lat = [49.4538163,49.1893459,48.0996548,49.2103917,47.7683835]
long = [7.5293362,8.3806152,7.3811118,8.1805128,9.2178378]

for i in range(len(lat)):
    string = "way(around:100," + str(lat[i]) + "," + str(long[i]) + ")[landuse];out tags center;"
    result = api.query(string)
    if (len(result.ways) > 0):
        landuse = ""
        for way in result.ways:
            landuse = landuse + way.tags.get("landuse", "n/a") + ", "
    else:
        landuse = "None"
    print("Coordinates: %f, %f, Landuse: %s" % (lat[i], long[i], landuse))