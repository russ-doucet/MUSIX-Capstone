import { React, useState, useEffect } from "react";
import { StyleSheet, View } from "react-native";

const Friends = () => {
  const style_one = {
    flex: 2,
    flexDirection: "row",
    marginTop: "0px",
    justifyContent: "space-evenly",
    padding: 20,
  };

  const styles = StyleSheet.create({
    container: {
      flex: 1,
      flexDirection: "column",
      margin: "auto",
      marginTop: "0px",
      //padding: 20,
    },
  });

  //Define state vars to track form inputs
  const [newFriend, setnewFriend] = useState("");
  const [friends, setFriends] = useState("");
  const [unfriend, setUnfriend] = useState("");

  /**
   * On page load, get our list of friends from the backend and update friends state
   */
  useEffect(() => {
    //Endpoint returns a list of dictionaries 
    //[{"email": "f1", "status": "outbound"}, {"email": "f2", "status": "friend"}...]
    fetch("api/get_friends")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setFriends(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, []);

  /**
   * Call add friend endpoint with the form input state var
   */
  const handleFriendRequest = async (e) => {
    e.preventDefault();

    const response = await fetch("api/add_friend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ friend: newFriend }),
    });

    if (response.ok) {
      alert("Added friend successful"); // Display success message
      setnewFriend("");
    } else {
      alert("Add friend failed"); // Display error message
      setnewFriend("");
    }

    //Refetch our list of all friends and update state
    fetch("api/get_friends")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setFriends(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  /**
   * Call the remove friend endpoint with the form input state var
   */
  const handleUnfriendRequest = async (e) => {
    e.preventDefault();

    const response = await fetch("api/remove_friend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ friend: unfriend }),
    });

    if (response.ok) {
      alert("removed friend successfully"); // Display success message
      setUnfriend("");
    } else {
      alert("remove friend failed"); // Display error message
      setUnfriend("");
    }

    //Retetch our list of all friends and update state
    fetch("api/get_friends")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setFriends(data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  };

  return (
    <>
      <View style={styles.container}>
        {/* Create two input fields and buttons for adding a friend and removing a friend */}
        <View style={style_one}>
          <div>
            <form onSubmit={handleFriendRequest}>
              <label>
                <label>
                  New Friend Email:
                  <input
                    type="email"
                    placeholder="Enter an email..."
                    name="friend"
                    onChange={(e) => setnewFriend(e.target.value)}
                    value={newFriend}
                  />
                </label>
                <input type="submit" value="Submit" />
              </label>
            </form>
          </div>
          <div>
            <form onSubmit={handleUnfriendRequest}>
              <label>
                <label>
                  Eliminate Friend
                  <input
                    type="email"
                    placeholder="Enter an email..."
                    name="Non-friend"
                    onChange={(e) => setUnfriend(e.target.value)}
                    value={unfriend}
                  ></input>
                </label>
                <input type="submit" value="Submit" />
              </label>
            </form>
          </div>
        </View>
        {/* Create a table that displays friends and their current friend status */}
        <View>
          <table className="table table-striped table-bordered">
            <thead>
              <tr>
                <th>Email</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {friends &&
                friends.map((friend) => (
                  <tr>
                    <td>{friend.email}</td>
                    <td>{friend.status}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </View>
      </View>
    </>
  );
};

export default Friends;
