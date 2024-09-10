import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import AboutUs from './components/AboutUs';
import HowItWorks from './components/HowItWorks';
import KeyFeatures from './components/KeyFeatures';
import SkillTokenization from './components/SkillTokenization';
import EmployerAccess from './components/EmployerAccess';
import Testimonials from './components/Testimonials';
import './App.css';

function App() {
  return (
    <div>
      <Header />
      <Hero />
      <AboutUs />
      <HowItWorks />
      <KeyFeatures />
      <SkillTokenization />
      <EmployerAccess />
      <Testimonials />
    </div>
  );
}

export default App;
