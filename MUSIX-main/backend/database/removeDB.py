import pymongo
"""
Delete a song from the database by location and name
Args: db (a mongodb database object)
      latitude: see writeSongCoordinates
      longitude: see writeSongCoordinates
      songName: see **
      maxDist: Maximum distance from the lat and long location we will consider

returns: <pymongo.results.DeleteResult object> or None

"""
def deleteSongCoordinateDB(coll, latitude : float, longitude : float, songName : str, maxDist = 1):
    query = {"loc" : {
                     "$near" : {
                               "$geometry" : {"type" : "Point", "coordinates" : [longitude, latitude]},
                               "$maxDistance" : maxDist
                               }
                     },
              "name" : songName
            }
    delete = None
    try:
        delete = coll.delete_one(query)
        return delete
    except:
        return None
    

