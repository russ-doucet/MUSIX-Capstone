import styled from "styled-components";

export const MapContainer = styled.div`
  align: flex;
  width: 50%;
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

export const ButtonContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;

  button {
    margin-right: 1rem;
  }
`;
