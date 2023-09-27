# MUSIX
A new approach to social-media. Share songs that are hot in your geographic region. Find and explore new popular hits

## Guide to the repository

The backend top-level directory contains python source code for the backend and database interface routines. These backend routines provide api-endpoints for a number of interactive features in our webapp

    The database subdirectory is a python module implementing CRUD (Create, read, update, and delete) operations on database collection items relevant to the webapp

The react-musix top-level directory contains the javascript source for our webpage, based primarily on the react framework

The test top-level directory contains source for testing js and python routines

The config top-level directory contains private information necessary for running the webapp. This directory is empty for non-team members


## Instructions for use

The webapp is deployed and hosted at (insert url here). 
1. Users may create an account by navigating to the login tab and filling out the necessary information. 
    
    a. Users will then be navigated back to the map/home page 
 

2. Once logged in users may be dump songs by entering a song-name and it's geographic location in the form on the bottom of the window. 
    a. The map will update after a few seconds a show a heatmap of songs "dumped" on the syracuse university quad.
    b. Users should feel free to navigate to other regions on the map and dump songs there as well to contribute to the geography of music. 
    c. The form defaults to the center of the current viewing window on the map

3. Users can create a new playlist sampling up to 20 songs in a paritcular window of the map by double clicking anywhere on the map!
    a. The playlist will be created and added to the User's playlist-list
    b. The newly added playlist will be named "hh:mm" where hh is the current hour and mm the current minute

4. Users may add and view their friends on the webapp
    a. Navigate to the friends tab by clicking "Friends" in the navbar on the top of the window
    b. Enter an email address of a friend (they don't even need to be signed up yet) to send an outbound friend request in the form on the top left labeled "New Friend Email"
    c. Click submit to send the request
    d. The table will update to show you your current friends list including inbound and outbound requests
    e. If a user has an inbound request, to mutually accept the request, the user needs to follow steps b and c above for the email address corresponding to the inbound request

5. Users may eliminate friends from their list on the webapp
    a. Simply enter an email address of someone you want removed from your friends list in the form labeled "Eliminate friend"
    b. Click submit to eliminate them from your list

## Instructions for testing users

1. Contact Matt C or Chris V to be granted a mongodb.config file and googlemaps.config file with temporary api keys for testing the project

2. Clone the repository from the command line <code> git clone *repository-url* </code> or download the zip

3. Place the mongodb.config file and googlemaps.config file in the config directory in the MUSIX project folder

4. Pip install the necessary python components for testing the project from requirements.txt

5. Compile the webapp by navigating to the react-musix directory and running <code>npm install; npm run build</code>

6. Navigate to the backend directory

7. Run the command <code> flask run </code> or <code> python app.py </code>


