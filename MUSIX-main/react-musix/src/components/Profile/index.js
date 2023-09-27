import React from "react";
import { ProfileContainer, ProfileElem, PlaylistWrapper, PlaylistTitle, SongList, SongItem, ButtonContainer, PopupStyles } from "./ProfileElements";
import { useState } from "react";
import Modal from "react-modal";

const Profile = (props) => {
  //Define state variables for rename popup
  const [isModalOpen, setIsModalOpen] = useState(false)
  /**
   * Used on rename button click
   * Mark old playlist name and open rename popup
   */
  const renamePlayList = (name) => {
    props.setOldName(name);
    setIsModalOpen(true);
  }

  /**
   * Given a dictionary of playlists, return the styled frontend displaying the playlist with rename and delete buttons
   * @param playlists Dict of playlist_name: list of songs
   */
  const Playlist = ({ name, songs }) => (
    <PlaylistWrapper>
      <PlaylistTitle><u>{name}</u></PlaylistTitle>
      <SongList>
        {songs.map((song) => (
          <SongItem key={song}>{song}</SongItem>
        ))}
      </SongList>
      {/* Add two buttons, delete playlist, and rename playlist */}
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        {<button style={{ borderRadius: '5px' }} onClick={() => props.removePlaylist(name)}>Delete</button>}
        {<button style={{ borderRadius: '5px' }} onClick={() => renamePlayList(name)}>Rename</button>}
      </div>
    </PlaylistWrapper>

  );
  return (
    <ProfileContainer>
      <h4 style={{ color: "black" }}>{props.isLoggedIn ? `Hello ${props.name}! Single left click to dump, right click to create a playlist` : ""}</h4>
      {props.isLoggedIn ?
        <ProfileElem>
          {/* If we are logged in, map each playlist to the front component to display them */}
          {Object.entries(props.playlists).map(([name, songs]) => (
            <Playlist key={name} name={name} songs={songs} />
          ))}
        </ProfileElem> :
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <h5>Please login to access your playlists</h5>
        </div>

      }
      {/* Define the popup that appears on renaming a playlist */}
      <Modal isOpen={isModalOpen}
        onRequestClose={() => setIsModalOpen(false)}
        style={PopupStyles}>
        <h2>Rename Playlist</h2>
        <label>
          New Name:
          <input
            type="text"
            placeholder="Enter a new name..."
            name="newName"
            onChange={(e) => props.setNewName(e.target.value)}
            value={props.newName}
          />
        </label>
        <ButtonContainer>
          {/* On clicking rename, update the name and then close the popup */}
          <button onClick={() => props.handleNameUpdate() && setIsModalOpen(false)}>Rename</button>
          <button onClick={() => setIsModalOpen(false)}>Close</button>
        </ButtonContainer>
      </Modal>
    </ProfileContainer>

  );
};

export default Profile;
