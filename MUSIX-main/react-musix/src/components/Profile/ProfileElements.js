import styled from "styled-components";

export const ProfileContainer = styled.div`
  background: radial-gradient(343px at 46.3% 47.5%, rgb(242, 242, 242) 0%, rgb(241, 241, 241) 72.9%);
  border-top: thin solid black;
  border-left: thin solid black;
  border-right: thin solid black;
  border-bottom: thin solid black;
  text-align: center;
  float: left;
  width: 50%;
  height: 100%;
`;

export const ProfileElem = styled.div`
  padding-top: 5px;
  color: white;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  height: 760px;

  @media (min-height: 760px) {
    overflow-x: auto;
  }
`;

export const PlaylistWrapper = styled.div`
  border: 1px solid #ccc;
  padding: 2rem;
  width: 80%;
  margin: 1rem auto;
  max-width: 400px;
  color: black;
  border-radius: 7px;
  background-color: #fff;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5);
`;

export const PlaylistTitle = styled.h2`
  margin: 0;
`;

export const SongList = styled.ul`
  margin: 0;
  padding: 0;
  list-style: none;
`;

export const SongItem = styled.li`
  margin-bottom: 0.5rem;
`;

export const ButtonContainer = styled.div`
  display: flex;
  justifyContent: center;
  align-items: center;
  width: 100%;

  button {
    margin-right: 1rem;
  }
`;
export const PopupStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
};