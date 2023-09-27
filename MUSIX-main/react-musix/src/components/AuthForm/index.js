import React from "react";
import { useState } from "react";
import "./index.css";

const AuthForm = (props) => {
  //Define state variables for tracking sign up vs log in form
  const [authMode, setAuthMode] = useState("signin");

  //Define state variables for form content
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  /**
   * Make post request to sign up endpoint using data from state variables
   * On success, set isLoggedIn state and redirect to homepage
   */
  const handleSignUpSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch("api/sign_up", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ "name": name, "email": email, "password": password }),
    });

    if (response.ok) {
      alert("Signup successful"); // Display success message
      props.setIsLoggedIn(true); //Mark as logged in
      window.location.href = "/"; //Redirect to home page
    } else {
      alert("Signup failed"); // Display error message
    }
  };

  /**
   * Make post request to sign in endpoint using data from state variables
   * On success, set isLoggedIn state and redirect to homepage
   */
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    // insert backend code here
    const response = await fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });
    if (response.ok) {
      props.setIsLoggedIn(true); //Mark as logged in
      window.location.href = "/"; //Redirect to home page
    } else {
      // Handle error
      alert("Account does not exist or email address and password do not match");
    }
  };

  const changeAuthMode = () => {
    setAuthMode(authMode === "signin" ? "signup" : "signin");
  };

  //Display either the sign up or sign in form based on authMode state var
  if (authMode === "signin") {
    return (
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={handleLoginSubmit}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Return User</h3>
            <div className="text-center">
              Not registered yet?{" "}
              <span className="link-primary" onClick={changeAuthMode}>
                Sign Up
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Email address</label>
              <input
                type="email"
                className="form-control mt-1"
                placeholder="Enter email"
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                className="form-control mt-1"
                placeholder="Enter password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                SIGN IN
              </button>
            </div>
          </div>
        </form>
      </div>
    );
  }

  return (
    <>
      <div className="Auth-form-container">
        <form className="Auth-form" onSubmit={handleSignUpSubmit}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">New User</h3>
            <div className="text-center">
              Already registered?{" "}
              <span className="link-primary" onClick={changeAuthMode}>
                Sign In
              </span>
            </div>
            <div className="form-group mt-3">
              <label>Full Name</label>
              <input
                type="name"
                className="form-control mt-1"
                placeholder="e.g Daniel Ek"
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <label>Email address</label>
              <input
                type="email"
                className="form-control mt-1"
                placeholder="Email Address"
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="form-group mt-3">
              <label>Password</label>
              <input
                type="password"
                className="form-control mt-1"
                placeholder="Password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                SIGN UP
              </button>
            </div>
          </div>
        </form>
      </div>
    </>
  );
};

export default AuthForm;
