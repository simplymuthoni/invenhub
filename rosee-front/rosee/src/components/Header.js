import React from 'react';

function Header() {
  return (
    <header>
      <div className="logo">
        <img src="/path/to/rose-logo.png" alt="Rosee Logo" />
        <h1>Rosee Thrifts</h1>
      </div>
      <nav>
        <ul>
          <li><a href="/login">Login</a></li>
          <li><a href="/shop">Shop</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
