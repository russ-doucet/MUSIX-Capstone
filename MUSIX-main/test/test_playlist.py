import unittest
from pymongo import MongoClient
import json
import sys
import requests
sys.path.append("../backend/")
import app
host = "127.0.0.1:5000"


class TestPlaylistMethods(unittest.TestCase):
    def test_add_to_playlist(self):
        # Test sending a request
        with self.client as c:
            # Log in as a user
            res = c.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Add songs to playlist
            c.post("/api/add_to_playlist",
                   json={"playlist": "p1", "song": "s1"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p1", "song": "s2"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p2", "song": "s3"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p2", "song": "s4"})
            # Check its in the db
            r1 = [i["song"] for i in self.playlists.find(
                {"user": "j@j.j", "playlist": "p1"})]
            r2 = [i["song"] for i in self.playlists.find(
                {"user": "j@j.j", "playlist": "p2"})]
            assert (r1 == ["s1", "s2"])
            assert (r2 == ["s3", "s4"])
            # Remove from the db
            self.playlists.delete_one(
                {"user": "j@j.j", "playlist": "p1", "song": "s1"})
            self.playlists.delete_one(
                {"user": "j@j.j", "playlist": "p1", "song": "s2"})
            self.playlists.delete_one(
                {"user": "j@j.j", "playlist": "p2", "song": "s3"})
            self.playlists.delete_one(
                {"user": "j@j.j", "playlist": "p2", "song": "s4"})

    def test_remove_from_playlist(self):
        # Test removing from playlist
        with self.client as c:
            # Log in as a user
            res = c.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Add song to playlist
            c.post("/api/add_to_playlist",
                   json={"playlist": "p1", "song": "s1"})
            # Verify it exists
            play = list(self.playlists.find(
                {"user": "j@j.j", "playlist": "p1"}))
            assert (play)
            # Remove song
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p1", "song": "s1"})
            # Verify it is gone
            play = list(self.playlists.find(
                {"user": "j@j.j", "playlist": "p1"}))
            assert (not play)

    def test_get_playlists(self):
        # Test sending a request
        with self.client as c:
            # Log in as a user
            res = c.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Add songs to playlist
            c.post("/api/add_to_playlist",
                   json={"playlist": "p1", "song": "s1"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p1", "song": "s2"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p2", "song": "s3"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p2", "song": "s4"})
            res = c.get("/api/get_playlists")
            assert (res.json == {"p1": ["s1", "s2"], "p2": ["s3", "s4"]})
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p1", "song": "s1"})
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p1", "song": "s2"})
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p2", "song": "s3"})
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p2", "song": "s4"})

    def test_get_playlist(self):
        # Test sending a request
        with self.client as c:
            # Log in as a user
            res = c.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Add songs to playlist
            c.post("/api/add_to_playlist",
                   json={"playlist": "p1", "song": "s1"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p1", "song": "s2"})
            c.post("/api/add_to_playlist",
                   json={"playlist": "p2", "song": "s3"})
            res = c.get("/api/get_playlist", query_string={"playlist": "p1"})
            print(res.json)
            assert (res.json == ["s1", "s2"])
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p1", "song": "s1"})
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p1", "song": "s2"})
            c.post("/api/remove_from_playlist",
                   json={"playlist": "p2", "song": "s3"})

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
            self.playlists = client.MusixUserData.Playlists

        # Start up the app
        self.app = app.app
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()


if __name__ == "__main__":
    unittest.main()
