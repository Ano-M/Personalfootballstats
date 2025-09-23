import React from "react";
import "./navbar.css";

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="navbar-left">anostat</div>
      <div className="navbar-right">Sign in</div>
    </nav>
  );
};

export default Navbar;
