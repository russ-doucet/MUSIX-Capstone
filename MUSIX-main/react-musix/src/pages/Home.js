import React from "react";
import { useState, useEffect } from "react";
import Profile from "../components/Profile";
import Map from "../components/Map";
import { StyleSheet, View } from "react-native";

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

const Home = (props) => {
  //State variables shared between us and map
  const [playlists, setPlaylists] = useState([]);
  const [center, setCenter] = useState({
    lat: 43.03767205440416,
    lng: -76.13400055373496,
  });
  const [song, setSong] = useState("");
  const [lat, setLat] = useState(center.lat);
  const [long, setLong] = useState(center.lng);
  const [oldName, setOldName] = useState("")
  const [newName, setNewName] = useState("")

  /**
   * On page load, get the user's playlists from the backend and update playlists state
   */
  useEffect(() => {
    async function getPlaylists() {
      const response = await fetch("/api/get_playlists_user");
      const data = await response.json();
      if (data != null) {
        setPlaylists(data);
      }
    }
    try {
      getPlaylists();
    } catch (err) {
      console.log("Error retrieving playlists");
    }
  }, [])

  /**
   * Call remove playlist endpoint to delete a playlist with name name for the user
   * @param {String} name The name of the playlist to remove
   * @returns boolean status of removal
   */
  const handleRemovePlaylist = async (name) => {
    const response = await fetch("api/remove_playlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ playlist: name }),
    });
    if (response.ok) {
      alert("Removal successful")
      window.location.reload();
      return true;
    } else {
      alert("Remove failed")
      return false;
    }
  };

  /**
   * Call the playlist rename endpoint using our state vars of the old and new name
   * @returns Boolean status of rename
   */
  const handleNameUpdate = async () => {
    const response = await fetch("api/update_playlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ curName: oldName, newName: newName }),
    });
    if (response.ok) {
      alert("Rename successful")
      window.location.reload();
      return true;
    } else {
      alert("Rename failed")
      return false;
    }
  };



  /**
   * Call the dump song endpoint with the song name, lat and long state vars
   * @returns Boolean status of dump
   */
  const handleDump = async () => {
    try {
      const response = await fetch("api/dump_song", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ song: song, lat: lat, long: long }),
      });
      if (response.ok) {
        alert("Dump successful"); // Display success message
        setSong("");
        setLat("");
        setLong("");
        return true;
      } else {
        throw "Dump failed";
      }
    } catch (err) {
      alert("Dump failed"); // Display error message
      setSong("");
      setLat("");
      setLong("");
      return false;
    }
  }

  return (
    <>
      <View
        style={[
          styles.container,
          {
            flexDirection: "row",
            flex: 2,
          },
        ]}
      >
        <Profile
          //Pass down state updaters and functions to the playlist to handle renaming and removing playlists
          playlists={playlists}
          isLoggedIn={props.isLoggedIn}
          setIsLoggedIn={props.setIsLoggedIn}
          name={props.name}
          removePlaylist={handleRemovePlaylist}
          setOldName={setOldName}
          setNewName={setNewName}
          newName={newName}
          handleNameUpdate={handleNameUpdate}
        />
        <Map
          //Pass down state updaters and functions to the map to handle dumping songs
          handleDump={handleDump}
          setPlaylists={setPlaylists}
          setSong={setSong}
          center={center}
          setCenter={setCenter}
          setLat={setLat}
          setLong={setLong}
        />
      </View>

    </>
  );
};

export default Home;
