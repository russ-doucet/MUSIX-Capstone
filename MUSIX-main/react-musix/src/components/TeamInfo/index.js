import React from "react";
import {
  PageWrapper,
  SectionWrapper,
  TeamWrapper,
  SubheadingWrapper,
} from "./TeamInfoElements";
// @author Russell Doucet
// Index file for the About Page

/* 
  Creating profile descriptions for everyone of our team members, we import the 
  JS components from the 'TeamInfoElements.js' file. I created a MainContainer to style 
  the profiles in a grid; with the respective team member descriptions applied to the components.
*/
// const TeamInfo = () => {
//   return (
//     <MainContainer>
//       <Header>Our Mission</Header>

//       {/* <AboutContainer>
//         MUSIX is a web application that allows users to sample their
//         geographically local music selection. Users are be able to link their
//         Spotify accounts to play MUSIX-generated playlists on our webpage! These
//         playlists will be generated from a random selection of geographically
//         correlated music other users have DUMPED into the local zone. DUMPS
//         expire after three weeks, reflecting the constantly evolving music
//         landscape. Users will have the option to save/generate playlists and
//         listen to them offsite (through Spotify directly), to DUMP songs, and to
//         add friends.
//       </AboutContainer> */}

//       <Statement>
//         Our mission is to make music sharing accessible by allowing users to
//         sample their geographically local music selection.
//       </Statement>

//       <Header>Our Vision</Header>

//       <Statement>

//       </Statement>

//       <Header>Meet Our Team!</Header>
//       <GridContainer>
//         <Member>Russell Doucet</Member>

//         <Member>Chenze Chen</Member>

//         <Member>Alex Haas</Member>

//         <Member>Matt Curfari</Member>

//         <Member>Saud lqabi</Member>

//         <Member>Chris Vinciguerra</Member>
//       </GridContainer>
//     </MainContainer>
//   );
// };
const TeamInfo = () => {
  return (
    <PageWrapper>
      <SectionWrapper>
        <h2>Our Mission</h2>
        <p>
          Our mission is to make music sharing accessible by allowing users to
          sample their geographically local music selection.
        </p>
      </SectionWrapper>
      <SectionWrapper>
        <h2>Our Story</h2>
        <p>
          To generate personalized playlists based on geographically correlated
          music other users have DUMPED into the local zone, reflecting the
          constantly evolving music landscape.
        </p>
      </SectionWrapper>
      <SectionWrapper>
        <h2>Meet Our Team</h2>
        <TeamWrapper>
          <SubheadingWrapper>
            <h3>Front-end Team</h3>
          </SubheadingWrapper>
          <ul>
            <li>
              <p>Chenze Chen</p>
            </li>
            <li>
              <p>Russell Doucet</p>
            </li>
            <li>
              <p>Alex Haas</p>
            </li>
          </ul>
        </TeamWrapper>
        <TeamWrapper>
          <SubheadingWrapper>
            <h3>Back-end Team</h3>
          </SubheadingWrapper>
          <ul>
            <li>
              <p>Matt Curfari</p>
            </li>
            <li>
              <p>Chris Vinciguerra</p>
            </li>
            <li>
              <p>Saud Alqabi</p>
            </li>
          </ul>
        </TeamWrapper>
      </SectionWrapper>
      <SectionWrapper>
        <h2>Legal Information</h2>
        <p>
          MUSIX reserves the right to keep some user data inside the database.
          The data is limited to usernames, emails, associated passwords, and
          MUSIX-generated song playlists. We have not and will not sell or give
          your data to any companies or third parties. MUSIX development team
          will notify its users of when and how we use the data.
        </p>
        <p>
          MUSIX development team reserves the right to change legal terms if
          needed. However, any changes directly involving our users will be
          preceded by a notification to said users about the changes.
        </p>
      </SectionWrapper>
    </PageWrapper>
  );
};

export default TeamInfo;
