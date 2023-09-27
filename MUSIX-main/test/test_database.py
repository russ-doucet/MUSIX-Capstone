
import unittest
from pymongo import MongoClient
import json
import sys
sys.path.append("../backend/")
from database.insertDB import writeSongCoordinateDB
from database.queryDB import querySongDB, querySongDB_Box
from database.removeDB import deleteSongCoordinateDB

class TestDatabaseMethods(unittest.TestCase):
    def test_insert_song(self):
        songName = "helloWorld"
        latitude = 50.1
        longitude = -75

        writeSucc = writeSongCoordinateDB(self.db, songName, latitude, longitude)
        self.assertTrue(writeSucc is not None)

    def test_query_db(self):
        latitude = 50.1
        longitude = -75
        querySuccess = querySongDB(self.db, latitude, longitude)
        self.assertTrue(querySuccess is not None)
       

    def test_query_db_box(self):
        min_lat = 50.0
        max_lat = 51.0
        min_long = -76.0
        max_long = -74.0
        querySuccess = querySongDB_Box(self.db, min_lat, max_lat, min_long, max_long)
        self.assertTrue(querySuccess is not None)
        

    def test_zdelete_song_coordinate(self):
        latitude = 50.1
        longitude = -75
        deleteSuccess = deleteSongCoordinateDB(self.db, latitude, longitude, songName = "helloWorld", maxDist = 1)
        self.assertTrue(deleteSuccess is not None)


    def setUp(self):
        db_username = None
        db_password = None
        self.db = None
        with open("../config/mongodb.config") as config_file:
            config = json.load(config_file)
            db_username = config["username"]
            db_password = config["password"]
            client = MongoClient(f"mongodb+srv://{db_username}:{db_password}@musixcluster.4gbtghn.mongodb.net/?retryWrites=true&w=majority")
            self.db = client.MusixUserData.SongLocations
    
if __name__ == "__main__":
    unittest.main()


