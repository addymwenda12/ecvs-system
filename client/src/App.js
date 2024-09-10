import React, { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import AboutUs from './components/AboutUs';
import HowItWorks from './components/HowItWorks';
import KeyFeatures from './components/KeyFeatures';
import SkillTokenization from './components/SkillTokenization';
import EmployerAccess from './components/EmployerAccess';
import Testimonials from './components/Testimonials';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [user, setUser] = useState(null);

  return (
    <div>
      <Header user={user} setUser={setUser} />
      {user ? (
        <Dashboard user={user} />
      ) : (
        <>
          <Hero />
          <AboutUs />
          <HowItWorks />
          <KeyFeatures />
          <SkillTokenization />
          <EmployerAccess />
          <Testimonials />
          <Login setUser={setUser} />
          <Register setUser={setUser} />
        </>
      )}
    </div>
  );
}

export default App;
