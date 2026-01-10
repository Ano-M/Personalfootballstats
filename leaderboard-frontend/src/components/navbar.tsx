import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { LoginForm } from "./LoginForm";
import { SignupForm } from "./SignupForm";
import "../styles/dark-theme.css";

const Navbar: React.FC = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');

  const handleSignInClick = () => {
    setAuthMode('login');
    setShowAuthModal(true);
  };

  const handleSwitchToSignup = () => {
    setAuthMode('signup');
  };

  const handleSwitchToLogin = () => {
    setAuthMode('login');
  };

  const handleCloseModal = () => {
    setShowAuthModal(false);
  };

  const handleLogout = () => {
    logout();
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-left">AnoStat</div>
        <div className="navbar-right">
          {isAuthenticated ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
              <span>{user?.email}</span>
              <button onClick={handleLogout} style={{
                background: 'transparent',
                border: '1px solid var(--foreground)',
                color: 'var(--foreground)',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Logout
              </button>
            </div>
          ) : (
            <span onClick={handleSignInClick} style={{ cursor: 'pointer' }}>
              Sign in
            </span>
          )}
        </div>
      </nav>

      {/* Auth Modal */}
      {showAuthModal && (
        <div className="modal-overlay" onMouseDown={handleCloseModal}>
          <div className="modal-content" onMouseDown={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={handleCloseModal}>×</button>
            {authMode === 'login' ? (
              <LoginForm
                onSwitchToSignup={handleSwitchToSignup}
                onClose={handleCloseModal}
              />
            ) : (
              <SignupForm
                onSwitchToLogin={handleSwitchToLogin}
                onClose={handleCloseModal}
              />
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default Navbar;
