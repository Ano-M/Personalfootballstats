import React from "react";
import "./player-info-card.css";

interface PlayerInfoCardProps {
  name: string;
  club: string;
  height: string;
  foot: string;
  dob: string; // e.g. "1995-05-12"
  imageUrl: string;
}

const calculateAge = (dob: string) => {
  const birthDate = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
};

const PlayerInfoCard: React.FC<PlayerInfoCardProps> = ({ 
  name, club, height, foot, dob, imageUrl 
}) => {
  return (
    <div className="player-card">
      <img src={imageUrl} alt={`${name} profile`} className="player-image" />
      <div className="player-details">
        <h2 className="player-name">{name}</h2>
        <p className="player-club">{club}</p>
        <div className="player-meta">
          <p><strong>Height:</strong> {height}</p>
          <p><strong>Foot:</strong> {foot}</p>
          <p><strong>Age:</strong> {calculateAge(dob)} ({dob})</p>
        </div>
      </div>
    </div>
  );
};

export default PlayerInfoCard;
