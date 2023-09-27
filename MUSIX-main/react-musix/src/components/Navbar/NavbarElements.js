import styled from "styled-components";

export const Nav = styled.div`
  background-color: #202020;
`;

export const NavContainer = styled.div`
  width: 90%;
  height: 80px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

export const NavMenu = styled.div`
  display: flex;
`;

export const NavItem = styled.div`
  padding: 10px 30px;
  @media (max-width: 400px) {
    padding: 10px 10px;
  }
`;
