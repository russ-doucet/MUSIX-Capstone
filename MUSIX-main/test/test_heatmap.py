import json
import unittest
from requests import Response
import requests
from pymongo import MongoClient

"""Tests the dump_song and dump_songs endpoint with a list of songs. Verify they were added to the database correctly"""
one = {"min_lat": 40, "max_lat": 45, "min_long": -75, "max_long": -72}


class TestHeatmapMethods(unittest.TestCase):
    def test_get_heatmap(self):
        res: Response = requests.post(
            "http://127.0.0.1:5000/api/heatmap", json=one)
        self.assertTrue(res.status_code == 200)
        # Query and verify
        print(res.json())

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
