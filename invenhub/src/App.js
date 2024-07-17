// src/App.js
import React from 'react';
import './App.css';
import Register from './components/Register';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import LoginPage from './LoginPage';
import Dashboard from './Dashboard'; // Create this component for after login

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>User Registration</h1>
                <Register />
            </header>
        </div>
    );
}

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/" exact component={LoginPage} />
        <Route path="/dashboard" component={Dashboard} />
      </Switch>
    </Router>
  );
};

export default App;
