import { React, useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Friends from "./pages/Friends";
import About from "./pages/About";
import Legal from "./pages/Legal";
import Home from "./pages/Home";
import SignInUp from "./pages/SignInUp";
import "bootstrap/dist/css/bootstrap.min.css";
import Navbar from "./components/Navbar";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [name, setName] = useState("");

  /**
   * On page load, check with the backend if we are logged in
   * If we are, update isLoggedIn state and name state vars
   */
  useEffect(() => {
    async function getLoginData() {
      const response = await fetch("/api/hello");
      const data = await response.json();
      if (data.isLoggedIn) {
        setIsLoggedIn(true);
        setName(data.name);
      } else {
        setIsLoggedIn(false);
      }
    }
    try {
      getLoginData();
    } catch (err) {
      console.log("Error in hello endpoint");
      setIsLoggedIn(false);
    }
  }, [isLoggedIn]);

  return (
    <Router>
      <Navbar
        isLoggedIn={isLoggedIn}
        setIsLoggedIn={setIsLoggedIn}
        name={name}
      />
      <Routes>
        <Route
          path="login"
          element={
            <SignInUp
              isLoggedIn={isLoggedIn}
              setIsLoggedIn={setIsLoggedIn}
              name={name}
            />
          }
        />
        <Route path="/" element={
          <Home
            isLoggedIn={isLoggedIn}
            setIsLoggedIn={setIsLoggedIn}
            name={name} />
        }
        />
        <Route path="friends" element={<Friends />} />
        <Route path="about" element={<About />} />
        <Route path="legal" element={<Legal />} />
      </Routes>
    </Router>
  );
}

export default App;
