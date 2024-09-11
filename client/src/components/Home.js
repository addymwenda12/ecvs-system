import React from 'react';
import { Link } from 'react-router-dom';
import Hero from './Hero';
import HowItWorks from './HowItWorks';
import KeyFeatures from './KeyFeatures';
import SkillTokenization from './SkillTokenization';
import EmployerAccess from './EmployerAccess';
import Testimonials from './Testimonials';
import ScanVerify from './ScanVerify';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <Hero />
      <main>
        <section className="features">
          <h2>Revolutionizing Credential Verification</h2>
          <div className="feature-grid">
            <div className="feature-item">
              <h3>Secure</h3>
              <p>Blockchain-backed credentials ensure tamper-proof records</p>
            </div>
            <div className="feature-item">
              <h3>Efficient</h3>
              <p>Instant verification for employers and institutions</p>
            </div>
            <div className="feature-item">
              <h3>Empowering</h3>
              <p>Students own and control their educational achievements</p>
            </div>
          </div>
        </section>
        <HowItWorks />
        <KeyFeatures />
        <SkillTokenization />
        <EmployerAccess />
        <ScanVerify />
        <Testimonials />
        <section className="cta">
          <h2>Ready to Get Started?</h2>
          <p>Join the future of credential verification today.</p>
          <Link to="/register" className="cta-button">Sign Up Now</Link>
        </section>
      </main>
    </div>
  );
}

export default Home;