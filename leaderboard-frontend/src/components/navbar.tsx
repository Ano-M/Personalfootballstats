import React from "react";
import "../styles/dark-theme.css";

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="navbar-left">anostat</div>
      <div className="navbar-right">Sign in</div>
    </nav>
  );
};

export default Navbar;
