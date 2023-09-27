import pymongo


"""
Query location of songs in database and pretty-print the values returned (temp)
Args: coll (a mongodb database collection object)
      latitude: see writeSongCoordinates
      longitude: see writeSongCoordinates

returns: <pymongo.cursor.Cursor object> or None
"""
def querySongDB(coll, latitude , longitude, maxDist = 1):
    docs = None
    try:
        docs = coll.find({"loc" : {
        "$near" : {
            "$geometry": {
                          "type": "Point",
                          "coordinates": [longitude, latitude]
                         },
        "$maxDistance": maxDist }
        }
        })
        return docs
    except:
        return None

"""
Query Song DB Box looks for documents that are indexed within the geo-rectangle passed to the function call
Args: coll 
      min_lat: smallest latitude value
      max_lat: largest latitude value
      min_long: smallest longitude value
      max_long: largest longitude value

returns <pymongo.cursor.Cursor object> or None
"""
def querySongDB_Box(coll, min_lat, max_lat, min_long, max_long):
    docs = None
    try: 
        docs = coll.find( { "loc" :
                         { "$geoWithin" :
                           { "$geometry" :
                             { "type" : "Polygon" ,
                               "coordinates" : [ [
                                                    [min_long,min_lat],
                                                    [min_long, max_lat],
                                                    [max_long, max_lat],
                                                    [max_long, min_lat],
                                                    [min_long, min_lat] 
                                               ] ]
                      } } } } )
        return docs
    except:
        return None