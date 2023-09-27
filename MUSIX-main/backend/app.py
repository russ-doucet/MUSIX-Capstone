from flask import Flask, request, session, redirect, send_from_directory
# from flask_cors import CORS
import bcrypt
import random
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
import json
from databaseHandlers import SongLocationsCollectionHandler, UsersCollectionHandler, FriendsCollectionHandler, FriendResponse, PlaylistCollectionHandler

# Initialize app
app = Flask(__name__, static_url_path='', static_folder='../react-musix/build')
app.secret_key = "14bc3f8ea403a640cf4cfe2c4d8c8f4a0c6b77afbe205592b8cb6ca152c8b192"
# CORS(app)
SLHandler = SongLocationsCollectionHandler()
UsersHandler = UsersCollectionHandler()
FriendsHandler = FriendsCollectionHandler()
PlaylistHandler = PlaylistCollectionHandler()


@app.route("/", defaults={'path': ''})
@app.route("/<path>")
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


# Initialize login manager
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(email):
    """
    Return a User object with the username if user exists
    Otherwise, return None
    """
    return UsersHandler.get_user(email)


@app.route("/api/sign_up", methods=["POST"])
def sign_up():
    """
    Sign up a new user
    Json requirements:
    username, email, password
    """
    json_data = request.get_json()
    salt = bcrypt.gensalt()
    data = {
        "name": json_data["name"],
        "email": json_data["email"],
        "salt": salt,
        "password": bcrypt.hashpw(json_data["password"].encode('utf-8'), salt)
    }
    # Check required parameters are in the form and are not empty
    if data["name"] is None or not data["name"] or data["email"] is None or not data["email"] or data["password"] is None or not data["password"]:
        return "Invalid sign up parameters", 400
    # Do simple email address validation
    if "@" not in data["email"] or "." not in data["email"] or not data["email"].isascii():
        return "Email format not valid", 400
    # Check if user already exists
    if load_user(data["email"]) is not None:
        return "User already exists with this email!", 400
    # Insert the data into the MongoDB collection
    UsersHandler.add_user(data)
    # Log in the user
    app.logger.info(f"Signing up user {data['email']}")
    succ = login_user(load_user(data["email"]))
    if not succ:
        return "Error in login", 400

    # Add name to session storage
    session["name"] = data["name"]
    # Redirect to another page
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/api/login", methods=["POST"])
def login():
    """
    Log in an existing user
    JSON requirements
    username, password
    """
    json_data: dict = request.get_json()
    email = json_data["email"]
    password = json_data["password"]
    # Check username and password are there
    if email is None or not email or password is None or not password:
        return "Username and password are required", 400

    successful = UsersHandler.authenticate_user(email, password)
    if not successful:
        return "Login failed", 400

    app.logger.info(f"Logging in user {email}")
    # Log in user
    succ = login_user(load_user(email))
    if not succ:
        return "Error in login", 400
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    """
    Logs a user out
    """
    logout_user()
    return "Successful"


@app.route("/api/dump_song", methods=["POST"])
def dump_song():
    """Add a new song to the database at a location"""
    # Gather info from request
    res = insert(request.get_json())
    if res is None:
        return "Error inserting song", 400
    return "Successful"


@app.route("/api/dump_songs", methods=["POST"])
def dump_songs():
    for i in request.get_json():
        res = insert(i)
        if res is None:
            return "Error inserting song", 400
    return "Successful"


@app.route("/api/heatmap", methods=["POST"])
def get_heatmap():
    bounds = request.get_json()
    app.logger.info(f"{bounds=}")
    try:
        min_lat = bounds["min_lat"]
        max_lat = bounds["max_lat"]
        min_long = bounds["min_long"]
        max_long = bounds["max_long"]
    except ValueError:
        return "Bounds does not contain required data", 400
    # Get song entries from database
    box = SLHandler.query_box(
        min_lat, max_lat, min_long, max_long)
    # Extract the coordinates of them
    locations = [doc["loc"]["coordinates"] for doc in box]
    # Reverse to be lat and then long to reflect google maps api
    locations = [(i[1], i[0]) for i in locations]
    app.logger.info(f"Returning: {locations}")
    return locations


@app.route("/api/get_friends", methods=["GET"])
@login_required
def get_friends():
    """
    Return a list of dictionaries of the names and emails of all friends of the current user
    """
    id = current_user.get_id()
    app.logger.info(f"Getting friends for {id}")
    return FriendsHandler.get_friends(id)


@app.route("/api/add_friend", methods=["POST"])
@login_required
def add_friend():
    """
    Sends a friend request to the user specified in the json
    """
    id = current_user.get_id()
    json_data = request.get_json()
    friend = json_data["friend"]
    app.logger.info(f"Sending request from {id} to {friend}")
    res = FriendsHandler.send_request(id, friend)
    if res == FriendResponse.REQUEST_SENT:
        app.logger.info("Sent friend request")
    elif res == FriendResponse.FRIENDSHIP_ADDED:
        app.logger.info("Friend added")
    return "Successful"


@app.route("/api/get_pending", methods=["GET"])
@login_required
def get_pending():
    """Returns a list of dictionaries of the names and emails of pending requests"""
    id = current_user.get_id()
    app.logger.info(f"Getting pending requests for {id}")
    return FriendsHandler.get_pending_friends(id)


@app.route("/api/remove_friend", methods=["POST"])
@login_required
def remove_friend():
    id = current_user.get_id()
    json_data = request.get_json()
    friend = json_data["friend"]
    app.logger.info(f"Removing friendship between {id} and {friend}")
    res = FriendsHandler.remove_friend(id, friend)
    if not res:
        app.logger.error("Error in removing friendship bet")
    return "Successful"


@app.route("/api/create_playlist_click", methods=["POST"])
@login_required
def create_playlist_click():
    json_data = request.get_json()
    minLong = json_data["min_long"]
    maxLong = json_data["max_long"]
    minLat = json_data["min_lat"]
    maxLat = json_data["max_lat"]
    songs = SLHandler.query_box_song(
        min_lat=minLat, max_lat=maxLat, min_long=minLong, max_long=maxLong)
    if songs:
        pl = PlaylistHandler.create_playlist(current_user.get_id(),
                                             random.sample(songs,
                                                           min(len(songs), 20)))
    else:
        app.logger.error("No songs found")
        return "Error creating playlist", 400
    return get_playlists_user()


@app.route("/api/get_playlists_user", methods=["GET"])
def get_playlists_user():
    if not current_user.get_id():
        return {"Login to view your playlists": ["Never gonna give you up"]}
    id = current_user.get_id()
    app.logger.info(f"Getting playlists for {id}")
    ret = PlaylistHandler.get_playlists(id)
    app.logger.info(f"Returning playlists: {ret}")
    return ret


@app.route("/api/remove_from_playlist", methods=["POST"])
@login_required
def remove_song_from_playlist():
    id = current_user.get_id()
    json_data = request.get_json()
    playlist = json_data["playlist"]
    song = json_data["song"]
    status = PlaylistHandler.remove_from_playlist(id, playlist, song)
    if not status:
        app.logger.error(
            f"Error removing {song} from playlist {playlist} for {id}")
        return "Error removing from playlist", 400
    return "Successful"


@app.route("/api/remove_playlist", methods=["POST"])
@login_required
def remove_playlist():
    id = current_user.get_id()
    json_data = request.get_json()
    playlist = json_data["playlist"]
    status = PlaylistHandler.remove_playlist(id, playlist)
    if not status:
        app.logger.error(f"Error removing playlist {playlist} for {id}")
        return "Error removing playlist", 400
    return "Successful"

# @app.route("/api/get_songs_playlist_userID", method=["POST"])
# @login_required
# def get_songs_playlist_userID():
#     id = current_user.get_id()
#     json_data = request.get_json()
#     playlist_id = json_data["playlist"]
#     return PlaylistHandler.get_playlist(id, playlist_id)


@app.route("/api/update_playlist", methods=["POST"])
@login_required
def update_playlist():
    id = current_user.get_id()
    json_data = request.get_json()
    newName = json_data["newName"]
    curName = json_data["curName"]
    if newName.isspace() or not newName:
        return "Error", 400
    
    stat = PlaylistHandler.update_name(id, curName, newName)
    if stat is None:
        return "Error", 400
    return "Successful"

@app.route("/api/hello")
def hello():
    data = {"isLoggedIn": False}
    try:
        data["name"] = current_user.name
        data["isLoggedIn"] = True
    except:
        pass
    return data


def insert(data):
    song = data["song"]
    lat = float(data["lat"])
    long = float(data["long"])
    if not song:
        return "Error", 400
    # Simply add to db
    return SLHandler.insert_song(song, lat, long)


if __name__ == "__main__":
    # Make sure DB connection is ok
    login_manager.init_app(app)
    app.run(debug=True)
