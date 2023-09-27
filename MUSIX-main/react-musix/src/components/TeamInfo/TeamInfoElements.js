import styled from "styled-components";
// @author: Russell Doucet
// Styling document for the about page.

/*
    This container is the styling container for the paragraph description
    of the app on the about page. The background is white to give the illusion
    of transparency with padding and margin adjustments in order to center the 
    text within the div box in an aesthetically pleasing way.
*/
export const PageWrapper = styled.div`
  max-width: 1000px;
  margin: 0 auto;
  padding-top: 40px;
  padding-left: 20px;
  padding-right: 20px;
`;

export const SectionWrapper = styled.section`
  margin-bottom: 50px;

  h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  p {
    font-size: 16px;
    line-height: 1.5;
  }
`;

export const TeamWrapper = styled.section`
  margin-bottom: 50px;

  h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }

  ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    list-style: none;
    padding: 0;
    justify-content: center;
  }

  li {
    background-color: #fff;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    text-align: center;
    border-radius: 5px;
    transition: all 0.3s ease-in-out;
  }

  p {
    text-align: center;
  }
`;

export const SubheadingWrapper = styled.div`
  margin-bottom: 20px;

  h3 {
    font-size: 18px;
    margin-bottom: 10px;
    color: #000;
  }
`;
