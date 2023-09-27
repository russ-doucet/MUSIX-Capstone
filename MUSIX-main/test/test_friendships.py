import unittest
from pymongo import MongoClient
import json
import sys
import requests
sys.path.append("../backend/")
import app
host = "127.0.0.1:5000"


class TestFriendshipMethods(unittest.TestCase):
    def test_send_request(self):
        # Test sending a request
        with self.client as c:
            # Log in as a user
            res = self.client.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Send the request
            c.post("/api/add_friend", json={"friend": "c@c.c"})
            # Check its in the db
            exists = self.requests.find_one({"from": "j@j.j", "to": "c@c.c"})
            assert (exists is not None)
            # Remove from the db
            self.requests.delete_one({"from": "j@j.j", "to": "c@c.c"})

    def test_fufilled_request(self):
        # Test sending a request from both users
        with self.client as c:
            # Log in as a user
            res = self.client.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Send the request
            c.post("/api/add_friend", json={"friend": "c@c.c"})
            # Check its in the db
            res = self.client.post(
                "/api/login", json={"email": "c@c.c", "password": "c"})
            # Send the request
            c.post("/api/add_friend", json={"friend": "j@j.j"})
            # Test that friendship is in db
            res1 = self.friends.find_one({"from": "j@j.j", "to": "c@c.c"})
            res2 = self.friends.find_one({"from": "c@c.c", "to": "j@j.j"})
            assert (res1 and res2)
            # Test that requests no longer exist
            res1 = self.requests.find_one({"from": "j@j.j", "to": "c@c.c"})
            res2 = self.requests.find_one({"from": "c@c.c", "to": "j@j.j"})
            assert (not res1 and not res2)
            # Delete the friendship
            res1 = self.friends.delete_one({"from": "j@j.j", "to": "c@c.c"})
            res2 = self.friends.delete_one({"from": "c@c.c", "to": "j@j.j"})

    def test_get_friends(self):
        # Test sending a request from both users
        with self.client as c:
            # Log in as a user
            res = self.client.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Send two outbound friend requests
            c.post("/api/add_friend", json={"friend": "c@c.c"})
            c.post("/api/add_friend", json={"friend": "e@e.e"})
            res = self.client.get("/api/get_friends")
            print(f"Outbound: {res.json}")
            assert (res.json == [
                    {'email': 'c@c.c', 'status': 'outbound'}, {'email': 'e@e.e', 'status': 'outbound'}])
            # Check its in the db
            res = self.client.post(
                "/api/login", json={"email": "c@c.c", "password": "c"})
            # Send the request
            c.post("/api/add_friend", json={"friend": "j@j.j"})
            # Relogin as original user
            res = self.client.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Now verify that the friend is in the get_friends request
            res = self.client.get("/api/get_friends")
            print(res.json)
            res1 = self.friends.delete_one({"from": "j@j.j", "to": "c@c.c"})
            res2 = self.friends.delete_one({"from": "c@c.c", "to": "j@j.j"})
            res3 = self.requests.delete_one({"from": "j@j.j", "to": "e@e.e"})
            assert (res1 and res2 and res3)

    # def test_get_pending(self):
    #     # Test sending a request
    #     with self.client as c:
    #         # Log in as a user
    #         res = self.client.post(
    #             "/api/login", json={"email": "j@j.j", "password": "j"})
    #         # Send the request outbound
    #         c.post("/api/add_friend", json={"friend": "d@d.d"})

    #         # Make a request inbound
    #         res = self.client.post(
    #             "/api/login", json={"email": "c@c.c", "password": "c"})
    #         # Send the request inbound
    #         c.post("/api/add_friend", json={"friend": "j@j.j"})

    #         res = self.client.post(
    #             "/api/login", json={"email": "j@j.j", "password": "j"})
    #         # Check pending
    #         res = self.client.get("/api/get_pending")
    #         print(res.json)
    #         assert (res.json == {"inbound": ["c@c.c"], "outbound": ["d@d.d"]})

    #         # Remove from the db
    #         self.requests.delete_one({"from": "j@j.j", "to": "d@d.d"})
    #         self.requests.delete_one({"from": "c@c.c", "to": "j@j.j"})

    def test_friend_remove(self):
        # Test sending a request from both users
        with self.client as c:
            # Log in as a user
            res = self.client.post(
                "/api/login", json={"email": "j@j.j", "password": "j"})
            # Send the request
            c.post("/api/add_friend", json={"friend": "c@c.c"})
            # Check its in the db
            res = self.client.post(
                "/api/login", json={"email": "c@c.c", "password": "c"})
            # Send the request
            c.post("/api/add_friend", json={"friend": "j@j.j"})
            # Test that friendship is in db
            res1 = self.friends.find_one({"from": "j@j.j", "to": "c@c.c"})
            res2 = self.friends.find_one({"from": "c@c.c", "to": "j@j.j"})
            assert (res1 and res2)
            # Remove the friendship
            c.post("/api/remove_friend", json={"friend": "j@j.j"})
            # Test that friendship no longer exist
            res1 = self.friends.find_one({"from": "j@j.j", "to": "c@c.c"})
            res2 = self.friends.find_one({"from": "c@c.c", "to": "j@j.j"})
            assert (not res1 and not res2)

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
            self.friends = client.MusixUserData.Friends
            self.requests = client.MusixUserData.FriendRequests

        # Start up the app
        self.app = app.app
        self.app.config.update({
            "TESTING": True,
        })
        self.client = self.app.test_client()


if __name__ == "__main__":
    unittest.main()
