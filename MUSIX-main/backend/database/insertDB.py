import pymongo

"""
write single song into database method:
Args: db (a mongodb database object)
      songName: a string containing the songname dumped here
      latitude: A float value between -90 and +90 with the latitude location of this dump
      longitude: A flaot value between -180 and +180 with the longitude location of this dump
    
side effects: db.SongLocations Collection contains a new entry to the song just dumped
Returns: True on success, None on exception
"""

def writeSongCoordinateDB(coll, songName: str, latitude : float, longitude : float):
    insertSucc = None
    try:
        coll.create_index([("loc", pymongo.GEOSPHERE)])
        coll.insert_one({
                "loc" : {"type": "Point", "coordinates":[longitude, latitude]},
                "name" : songName
            })
        
        return True
    except:
        return None


