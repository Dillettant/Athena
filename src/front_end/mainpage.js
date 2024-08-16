import React from 'react';
import styled from 'styled-components';

const DashboardContainer = styled.div`
  display: flex;
  height: 100vh;
  background-color: #f9f9f9;
`;

const Sidebar = styled.div`
  width: 250px;
  background-color: #2c2c2c;
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
`;

const ContentArea = styled.div`
  flex: 1;
  padding: 50px;
`;

const ProjectSelectorContainer = styled.div`
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-top: 50px;
`;

const ProjectCard = styled.div`
  width: 300px;
  height: 200px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s;
  
  &:hover {
    transform: translateY(-5px);
  }

  img {
    width: 60px;
    margin-bottom: 20px;
  }

  h3 {
    font-size: 18px;
    color: #333;
  }

  p {
    font-size: 14px;
    color: #777;
  }
`;

const CreditsSection = styled.div`
  margin-top: 50px;
  color: #b9b9b9;
  
  a {
    color: #fff;
    text-decoration: none;
    margin-top: 10px;
    display: block;
  }

  a:hover {
    color: #b9b9b9;
  }
`;

const UserProfile = styled.div`
  display: flex;
  align-items: center;
  padding: 20px 0;

  img {
    border-radius: 50%;
    width: 40px;
    height: 40px;
    margin-right: 10px;
  }

  p {
    color: #fff;
    font-size: 14px;
  }
`;

const Dashboard = () => {
  return (
    <DashboardContainer>
      <Sidebar>
        <div>
          <button>+ New Project</button>
          <CreditsSection>
            <p>2120 credits</p>
            <a href="#">Connect with us & earn free credits</a>
            <a href="#">Get 800 credits</a>
            <a href="#">Get 100 credits</a>
          </CreditsSection>
        </div>
        <UserProfile>
          <img src="/path-to-user-profile-image.jpg" alt="Wenyi Wu" />
          <p>Wenyi Wu</p>
        </UserProfile>
      </Sidebar>
      <ContentArea>
        <h2>What would you like to start working on today?</h2>
        <ProjectSelectorContainer>
          <ProjectCard>
            <img src="/path-to-paper-writer-icon.jpg" alt="Paper Writer" />
            <h3>Paper Writer</h3>
            <p>Write your paper from the beginning.</p>
          </ProjectCard>
          <ProjectCard>
            <img src="/path-to-paper-polisher-icon.jpg" alt="Paper Polisher" />
            <h3>Paper Polisher</h3>
            <p>Refine and perfect your paper.</p>
          </ProjectCard>
        </ProjectSelectorContainer>
      </ContentArea>
    </DashboardContainer>
  );
};

export default Dashboard;