import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AppNavbar from './components/Shared/Navbar';
import HomePage from './components/Home/Home';
import ItemList from './components/Items/ItemList';
import Cart from './components/Cart/Cart';
import Login from './components/Auth/Login';
import OAuthCallback from './components/Auth/OAuthCallback';
import Register from './components/Auth/Register';
import Payment from './components/Payment/Payment';
import Footer from './components/Shared/Footer';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';


function App() {
  return (
    <Router>
      <div>
        <AppNavbar />
        <Routes>
          <Route path="/" exact component={HomePage} />
          <Route path="/register" component={Register} />
          <Route path="/items" component={ItemList} />
          <Route path="/cart" component={Cart} />
          <Route path="/login/:provider" component={Login} />
          <Route path="/callback/:provider" component={OAuthCallback} />
          <Route path="/payment" component={Payment} />
          <ProtectedRoute path="/protected" component={ProtectedComponent} />
        </Routes>
        <Footer/>
      </div>
    </Router>
  );
}

function ProtectedComponent() {
  return <h3>Protected</h3>;
}

export default App;

// // app.js

// const express = require('express');
// const session = require('express-session');
// const passport = require('./passport');

// const app = express();

// // Session middleware
// app.use(session({ secret: 'your_secret_key', resave: false, saveUninitialized: false }));

// // Initialize Passport and restore authentication state, if any, from the session
// app.use(passport.initialize());
// app.use(passport.session());

// // Routes
// app.get('/', (req, res) => {
//   res.send('<h1>Home</h1><a href="/auth/google">Login with Google</a><br><a href="/auth/microsoft">Login with Microsoft</a><br><a href="/auth/apple">Login with Apple</a>');
// });

// // Google OAuth routes
// app.get('/auth/google', passport.authenticate('google', { scope: ['profile'] }));
// app.get('/auth/google/callback',
//   passport.authenticate('google', { failureRedirect: '/' }),
//   (req, res) => {
//     res.redirect('/profile');
//   }
// );

// // Microsoft OAuth routes
// app.get('/auth/microsoft', passport.authenticate('microsoft'));
// app.get('/auth/microsoft/callback',
//   passport.authenticate('microsoft', { failureRedirect: '/' }),
//   (req, res) => {
//     res.redirect('/profile');
//   }
// );

// // Apple OAuth routes
// app.get('/auth/apple', passport.authenticate('apple'));
// app.post('/auth/apple/callback',
//   passport.authenticate('apple', { failureRedirect: '/' }),
//   (req, res) => {
//     res.redirect('/profile');
//   }
// );

// app.get('/profile', (req, res) => {
//   if (req.isAuthenticated()) {
//     res.send(`<h1>Profile</h1><p>${JSON.stringify(req.user)}</p><a href="/logout">Logout</a>`);
//   } else {
//     res.redirect('/');
//   }
// });

// app.get('/logout', (req, res) => {
//   req.logout();
//   res.redirect('/');
// });

// const PORT = process.env.PORT || 3000;
// app.listen(PORT, () => {
//   console.log(`Server is running on port ${PORT}`);
// });
