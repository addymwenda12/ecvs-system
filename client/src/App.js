import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
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
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/dashboard" component={Dashboard} />
            <Route path="/institution" component={InstitutionInterface} />
            <Route path="/employer" component={EmployerInterface} />
            <Route path="/login" component={Login} />
            <Route path="/register" component={Register} />
          </Switch>
        </div>
      </Router>
    </Provider>
  );
}

export default App;