import React from "react";
import { ReactComponent as ReactLogo } from "./logo.svg";
import { NavLink } from "react-router-dom";
import {
  Nav,
  NavContainer,
  NavItem,
  NavMenu,
  WelcomeItem,
} from "./NavbarElements";

const Navbar = (props) => {
  const logoStyle = {
    width: "60px",
    height: "60px",
  };

  /**
   * Call logout endpoint, set isLoggedIn state to false
   */
  const logout = async () => {
    try {
      const response = await fetch("api/logout", {
        method: "POST",
      });
    } catch (err) {
    } finally {
      props.setIsLoggedIn(false);
    }
  };

  return (
    <>
      <Nav>
        <NavContainer>
          <NavLink to="/">
            <ReactLogo style={logoStyle} />
          </NavLink>
          <NavMenu>
            <NavItem>
              <NavLink
                to="/friends"
                style={({ isActive }) => ({
                  borderBottom: isActive ? "2px solid white" : "none",
                  padding: "2px",
                  textDecoration: "none",
                  color: "#f5f5f5",
                  cursor: "pointer",
                })}
              >
                Friends
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                to="/about"
                style={({ isActive }) => ({
                  borderBottom: isActive ? "2px solid white" : "none",
                  padding: "2px",
                  textDecoration: "none",
                  color: "#f5f5f5",
                  cursor: "pointer",
                })}
              >
                About Us
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                to="/login"
                style={({ isActive }) => ({
                  borderBottom: isActive ? "2px solid white" : "none",
                  padding: "2px",
                  textDecoration: "none",
                  color: "#f5f5f5",
                  cursor: "pointer",
                })}
                // When logged in, make clicking the button log us out
                onClick={props.isLoggedIn ? logout : null}
              >
                {/* Change the text to be login or logout based on what we are not */}
                {props.isLoggedIn ? "Logout" : "Login"}
              </NavLink>
            </NavItem>
          </NavMenu>
        </NavContainer>
      </Nav>
    </>
  );
};

export default Navbar;
