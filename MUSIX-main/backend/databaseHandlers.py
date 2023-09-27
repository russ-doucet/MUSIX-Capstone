from enum import Enum
import bcrypt
from flask_login import UserMixin
from pymongo import MongoClient
from database.queryDB import *
from database.insertDB import *
from database.removeDB import *
import json
from datetime import datetime


"""
Here we define a DatabaseHandler class that serves as a wrapper around the various database functions

    This handler is instantiated with a mongoDB database object and 
    assumes the collection name is the name provided in the database 
    managed by the MUSIX team

This handler will be created on app startup and provide a means of interfacing 
(CRUDING) between the backend and MONGODB service
"""


class DatabaseHandler():
    def __init__(self):
        db_username = None
        db_password = None
        with open("../config/mongodb.config") as f:
            config = json.load(f)
            db_username = config["username"]
            db_password = config["password"]
            # Connect to database
        self.client = MongoClient(
            f"mongodb+srv://{db_username}:{db_password}@musixcluster.4gbtghn.mongodb.net/test")
        self.db = self.client["MusixUserData"]
        result = self.client.admin.command('ping')
        if not result["ok"]:
            print("failed database connection")
            exit()
        else:
            print("Database ping successful")


class SongLocationsCollectionHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()
        self.collection = self.db.SongLocations

    def query_loc(self, latitude, longitude, maxDist=1):
        return querySongDB(self.collection, latitude, longitude, maxDist)

    def query_box(self, min_lat, max_lat, min_long, max_long):
        return querySongDB_Box(self.collection, min_lat, max_lat, min_long, max_long)

    def query_box_song(self, min_lat, max_lat, min_long, max_long):
        boxresult = self.query_box(min_lat, max_lat, min_long, max_long)
        songList = [doc["name"] for doc in boxresult]
        return songList

    def insert_song(self, songName, latitude, longitude):
        if songName.isspace() or not songName:
            return "Error", 400
        return writeSongCoordinateDB(self.collection, songName, latitude, longitude)

    def delete_song(self, latitude, longitude, songName, maxDist=1):
        return deleteSongCoordinateDB(self.collection, latitude, longitude, songName, maxDist)

    def __repr__(self):
        return "<SongLocationCollectionHandler object>"

    def __str__(self):
        return "SongLocationCollectionHandler"


class User(UserMixin):
    def __init__(self, data):
        self.email = data["email"]
        self.name = data["name"]

    def get_id(self):
        return self.email


class UsersCollectionHandler(DatabaseHandler):

    def __init__(self):
        super().__init__()
        self.collection = self.db.Users

    def __repr__(self):
        return "<UsersCollectionHandler object>"

    def __str__(self):
        return "UsersCollectionHandler"

    def get_user(self, email):
        """
        Return a user object using the data from the database
        If user does not exist, return None
        """
        data = self.collection.find_one({"email": email})
        if data:
            return User(data)
        return None

    def authenticate_user(self, email, password):
        """
        Return True if user exists and password is correct
        Returns False otherwise
        """
        data = self.collection.find_one({"email": email})
        attempted = password.encode("utf-8")
        true_password = data["password"]
        if not bcrypt.checkpw(attempted, true_password):
            return
        return True

    def add_user(self, data):
        """
        Add a user to the database
        Required in data: email, name, salt, password
        """
        self.collection.insert_one(data)


class FriendResponse(Enum):
    REQUEST_SENT = 1,
    FRIENDSHIP_ADDED = 2,


class FriendsCollectionHandler(DatabaseHandler):

    def __init__(self):
        super().__init__()
        self.friends = self.db.Friends
        self.requests = self.db.FriendRequests

    def get_friends(self, id):
        """
        Return a list of ids that are friends with the user
        """
        friend_ids = [{"email": f['to'], "status":"friend"}
                      for f in self.friends.find({'from': id})]
        inbound_requests = self.requests.find({'to': id})
        outbound_requests = self.requests.find({'from': id})
        inbound_ids = [{"email": request['from'], "status":"inbound"}
                       for request in inbound_requests]
        outbound_ids = [{"email": request['to'], "status":"outbound"}
                        for request in outbound_requests]
        return friend_ids + inbound_ids + outbound_ids

    def get_pending_friends(self, id):
        """
        Return a dictionary of inbound and outbound pending friend requests
        """
        inbound_requests = self.requests.find({'to': id})
        outbound_requests = self.requests.find({'from': id})
        inbound_ids = [{"email": request['from'], "status":"inbound"}
                       for request in inbound_requests]
        outbound_ids = [{"email": request['to'], "status":"outbound"}
                        for request in outbound_requests]
        return inbound_ids.append(outbound_ids)

    def remove_friend(self, id, friend_id):
        """
        Remove the friendship between id and friend_id
        """
        # Try remove request
        pending_res = self.requests.delete_one({"from": id, "to": friend_id})
        friend_one = self.friends.delete_one({"from": id, "to": friend_id})
        friend_two = self.friends.delete_one({"from": friend_id, "to": id})
        return pending_res or (friend_one and friend_two)

    def send_request(self, id, to_id):
        """
        Send a friend request to the to_id, and add a friendship if the request is two way
        """
        request = self.requests.find_one({"from": to_id, "to": id})
        if request is None:
            self.requests.insert_one({"from": id, "to": to_id})
            return FriendResponse.REQUEST_SENT
        else:
            self.friends.insert_many([{"from": id, "to": to_id},
                                      {"from": to_id, "to": id}])
            self.requests.delete_one({"from": to_id, "to": id})
            return FriendResponse.FRIENDSHIP_ADDED

   
    def __repr__(self):
        return "<FriendsCollectionHandler object>"

    def __str__(self):
        return "FriendsCollectionHandler"


class PlaylistCollectionHandler(DatabaseHandler):

    def __init__(self):
        super().__init__()
        self.playlists = self.db.Playlists

    def create_playlist(self, id, songs):
        name = datetime.now().strftime("%H:%M:%S")
        entries = [{"user": id, "playlist": name, "song": i} for i in songs]
        self.playlists.insert_many(entries)
        return self.get_playlist(id, name)

    def remove_playlist(self, id, name):
        res = self.playlists.delete_many({"user": id, "playlist": name})
        return res
    def add_to_playlist(self, id, playlist, song):
        if self.playlists.find_one({"user": id, "playlist": playlist, "song": song}):
            return False
        self.playlists.insert_one(
            {"user": id, "playlist": playlist, "song": song})

    def remove_from_playlist(self, id, playlist, song):
        if not self.playlists.find_one({"user": id, "playlist": playlist, "song": song}):
            return False
        self.playlists.delete_one({"user": id, "playlist": playlist, "song": song})
        return True

    def remove_playlist(self, id, playlist):
        if not self.playlists.find({"user": id, "playlist": playlist}):
            return False
        self.playlists.delete_many({"user": id, "playlist": playlist})
        return True

    def get_playlist(self, id, playlist_name):
        playlist = [i["song"] for i in self.playlists.find(
            {"user": id, "playlist": playlist_name})]
        return playlist

    def get_playlists(self, id):
        entries = list(self.playlists.find({"user": id}))
        playlists = {}
        for i in entries:
            if i["playlist"] not in playlists:
                playlists[i["playlist"]] = []
            playlists[i["playlist"]].append(i["song"])
        return playlists
    
    def update_name(self, id, curName, newName):
        """
        Update the name of a playlist
        """
        return self.playlists.update_many({"user":id,"playlist":curName},{ "$set": { "playlist": newName } })

    def __repr__(self):
        return "<PlaylistCollectionHandler object>"

    def __str__(self):
        return "PlaylistCollectionHandler"
