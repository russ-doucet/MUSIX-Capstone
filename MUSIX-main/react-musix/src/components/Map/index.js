import { MapContainer, ButtonContainer, PopupContainer, PopupStyles } from "./MapStyle";
import React, { useState, useRef, useMemo } from "react";
import { GoogleMap, LoadScript, HeatmapLayer } from "@react-google-maps/api";
import { debounce } from "lodash";
import Modal from "react-modal";
import googleMapsInfo from "./config/googlemaps.json";
//Define library used for the heatmap here to prevent reload weirdness
const libs = ["visualization"];

const Map = (props) => {

  const mapStyles = {
    height: "100%",
    width: "100%",
  };


  //Define state variable for dump popup
  const [isModalOpen, setIsModalOpen] = useState(false);

  //Define state variables for list of heatmap coordinates
  const [heatmapData, setHeatmapData] = useState([]);
  const mapRef = useRef(null);
  //Use useMemo for Google Maps HeatmapLayer, only reloading on new heatmap data
  const heatMapComp = useMemo(() => {
    return (
      <HeatmapLayer data={heatmapData} />)
  }, [heatmapData]
  );

  /**
   * Store the reference to the Google Map object on load
   */
  const onLoad = (map) => {
    mapRef.current = map;
  };

  /**
   * Given the map bounds object, get the list of coordinate tuples within those bounds from the api endpoint
   * Update the heatmapData state to cause the layer to reload
   */
  const fetchHeatmapData = async (bounds) => {
    console.log("Fetching, bounds are ", bounds);
    try {
      const { south, north, west, east } = bounds.toJSON();
      const response = await fetch("/api/heatmap", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          min_lat: south,
          max_lat: north,
          min_long: west,
          max_long: east,
        }),
      });
      const data = await response.json();
      //Map the raw tuples to LatLng objects for the HeatmapLayer
      const heatmapData = data.map(
        (pair) => new window.google.maps.LatLng(pair[0], pair[1])
      );
      //Set the data to cause a HeatmapLayer reload
      setHeatmapData(heatmapData);
    } catch (error) {
      console.error(error);
    }
  };

  /**
   * Given the map bounds object, call the playlist creation endpoint
   * Set the playlists state variables with the new complete list of playlists
   */
  const fetchCreatePlaylist = async (bounds) => {
    console.log("Fetching songs in bounds ", bounds);
    try {
      const { south, north, west, east } = bounds.toJSON();
      const response = await fetch("/api/create_playlist_click", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          min_lat: south,
          max_lat: north,
          min_long: west,
          max_long: east,
        }),
      });
      //Endpoint returns all of the playlists, including our new ones
      const playlists = await response.json();
      //Set the playlist state to update their display as another comp
      props.setPlaylists(playlists);
      if (response.ok) {
        alert("Added playlist successfully"); // Display success message
      }
    } catch (error) {
      alert("Add playlist failed");// Display error message
      console.error(error);
    }
  };

  //Create debounced versions to prevent overloading API calls when dragging the map around
  const debouncedFetchHeatmapData = debounce(fetchHeatmapData, 500);
  const debouncedFetchCreatePlaylist = debounce(fetchCreatePlaylist, 500);

  /**
   * Fetch the new heatmap data when we move the map around (if debounced timeout expired)
   */
  const onBoundsChanged = () => {
    if (mapRef.current) {
      const bounds = mapRef.current.getBounds();
      if (!bounds) {
        return;
      }
      debouncedFetchHeatmapData(bounds);
    }
  };

  /**
   * Fetch new heatmap data upon dumping a new song to display the new song
   */
  const dumpDate = async () => {
    if (mapRef.current) {
      const bounds = mapRef.current.getBounds();
      if (!bounds) {
        return;
      }
      fetchHeatmapData(bounds)
    }
  }

  /**
   * On a map click, update latitude and longitude state of where we clicked, and open the dump popup
   */
  const handleClick = (mapClick) => {
    props.setLat(mapClick.latLng.lat());
    props.setLong(mapClick.latLng.lng())
    setIsModalOpen(true);
  }


  /**
   * On a map right click, create a new playlist using the current map bounds
   */
  const handleRightClick = (mapClick) => {
    if (mapRef.current) {
      const bounds = mapRef.current.getBounds();
      props.setCenter(mapRef.current.getCenter());
      props.setLat(props.center.lat);
      props.setLong(props.center.lng);
      debouncedFetchCreatePlaylist(bounds);
    }
  };

  return (
    <MapContainer>
      <LoadScript
        googleMapsApiKey={googleMapsInfo.api_key}
        libraries={libs}
      >
        <GoogleMap
          mapContainerStyle={mapStyles}
          zoom={15}
          center={props.center}
          onLoad={onLoad}
          onBoundsChanged={onBoundsChanged}
          onClick={handleClick}
          onRightClick={handleRightClick}
        >
          {heatMapComp}
        </GoogleMap>
      </LoadScript>
      <Modal isOpen={isModalOpen}
        onRequestClose={() => setIsModalOpen(false)}
        style={PopupStyles}>
        <h2>Dump Song</h2>
        <label>
          Song:
          <input
            type="text"
            placeholder="Enter a song..."
            name="song"
            onChange={(e) => props.setSong(e.target.value)}
            value={props.song}
          />
        </label>
        <ButtonContainer>
          {/* When pressing dump button, call handle dump, reload the heatmap data, and close the popup */}
          <button onClick={() => props.handleDump() && dumpDate() && setIsModalOpen(false)}>Dump</button>
          <button onClick={() => setIsModalOpen(false)}>Close</button>
        </ButtonContainer>
      </Modal>
    </MapContainer>
  );
};

export default Map;
