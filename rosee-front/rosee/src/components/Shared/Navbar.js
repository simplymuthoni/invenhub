import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav } from 'react-bootstrap';

function AppNavbar() {
  return (
    <>
      <head>
        <style>
          {`
          .navigation {
            position: relative;
            width: 400px;
            height: 70px;
            background: linear-gradient(155deg, #00fffc, #eee);
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 10px;
          }
          .navigation ul li {
            position: relative;
            width: 70px;
            height: 70px;
            list-style: none;
            z-index: 1;
          }
          .indicator {
            position: absolute;
            top: -50%;
            width: 70px;
            height: 70px;
            background: linear-gradient(0deg, #eee, #00fffc);
            border: 6px solid #06021b;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: .5s;
          }
          .navigation ul {
            transform: translateY(-32px);
          }
          `}
        </style>
      </head>
      <Navbar bg="light" expand="lg">
        <Navbar.Brand as={Link} to="/">Rosee Thrifts</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link as={Link} to="/">Home</Nav.Link>
            <Nav.Link as={Link} to="/items">Shop</Nav.Link>
            <Nav.Link as={Link} to="/cart">Cart</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    </>
  );
}

export default AppNavbar;
