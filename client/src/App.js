import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
import Header from './components/Header';
import Home from './components/Home';
import Dashboard from './components/Dashboard';
import InstitutionInterface from './components/InstitutionInterface';
import EmployerInterface from './components/EmployerInterface';
import Login from './components/Login';
import Register from './components/Register';
import NotificationSystem from './components/NotificationSystem';

function App() {
  return (
    <Provider store={store}>
      <Router>
        <div>
          <Header />
          <NotificationSystem />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/institution" element={<InstitutionInterface />} />
            <Route path="/employer" element={<EmployerInterface />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </div>
      </Router>
    </Provider>
  );
}

export default App;