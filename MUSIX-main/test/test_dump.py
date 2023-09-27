from pymongo import MongoClient
import sys
sys.path.append("../backend/")
from database.removeDB import deleteSongCoordinateDB
from database.queryDB import querySongDB
import requests
from requests import Response
import unittest
import json

"""Tests the dump_song and dump_songs endpoint with a list of songs. Verify they were added to the database correctly"""
one = {"song": "Musix", "lat": 42.646, "long": -73.723}
data = [{"song": "Happy Birthday", "lat": 42.641572, "long": -73.766067},
        {"song": "Mirrors", "lat": 42.6, "long": -73.8},
        {"song": "Patty Cake", "lat": 42.642, "long": -73.763},
        {"song": "Friends in Paris", "lat": 42.4, "long": -73.4}]


class TestDatabaseMethods(unittest.TestCase):
    def test_dump_song(self):
        res: Response = requests.post(
            "http://127.0.0.1:5000/api/dump_song", json=one)
        self.assertTrue(res.status_code == 200)
        # Query and verify
        queryStatus = querySongDB(self.db, one["lat"], one["long"])
        self.assertTrue(queryStatus is not None)
        deleteStatus = deleteSongCoordinateDB(
            self.db, one["lat"], one["long"], songName=one["song"], maxDist=1)
        self.assertTrue(deleteStatus is not None)

    def test_dump_songs(self):
        res: Response = requests.post(
            "http://127.0.0.1:5000/api/dump_songs", json=data)
        self.assertTrue(res.status_code == 200)
        for song in data:
            queryStatus = querySongDB(self.db, song["lat"], song["long"])
            self.assertTrue(queryStatus is not None)
            deleteStatus = deleteSongCoordinateDB(
                self.db, song["lat"], song["long"], songName=song["song"], maxDist=1)
            self.assertTrue(deleteStatus is not None)

    def setUp(self):
        db_username = None
        db_password = None
        self.db = None
        with open("../config/mongodb.config") as config_file:
            config = json.load(config_file)
            db_username = config["username"]
            db_password = config["password"]
            client = MongoClient(
                f"mongodb+srv://{db_username}:{db_password}@musixcluster.4gbtghn.mongodb.net/?retryWrites=true&w=majority")
            self.db = client.MusixUserData.SongLocations


if __name__ == "__main__":
    unittest.main()
