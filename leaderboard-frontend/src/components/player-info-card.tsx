import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import "../styles/dark-theme.css";

interface UserStats {
  totalMatches: number;
  totalGoals: number;
  totalAssists: number;
  averageRating: number;
}

const PlayerInfoCard: React.FC = () => {
  const { user, isAuthenticated } = useAuth();
  const [stats, setStats] = useState<UserStats>({
    totalMatches: 0,
    totalGoals: 0,
    totalAssists: 0,
    averageRating: 0,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      fetchUserStats();
    }
  }, [isAuthenticated]);

  const fetchUserStats = async () => {
    try {
      setLoading(true);
      const leaderboard = await api.stats.getLeaderboard();

      if (leaderboard.length > 0) {
        const totalMatches = leaderboard.length;
        const totalGoals = leaderboard.reduce((sum, match) => sum + match.goals, 0);
        const totalAssists = leaderboard.reduce((sum, match) => sum + match.assists, 0);
        const averageRating = leaderboard.reduce((sum, match) => sum + match.rating, 0) / totalMatches;

        setStats({
          totalMatches,
          totalGoals,
          totalAssists,
          averageRating,
        });
      }
    } catch (error) {
      console.error('Failed to load user stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="player-card" style={{ background: 'var(--card)', maxWidth: '800px', margin: '2rem auto' }}>
        <div style={{ padding: '2rem', textAlign: 'center' }}>
          <h2>Welcome to AnoStat</h2>
          <p>Please sign in to view your stats and track your football performance</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="player-card" style={{ background: 'var(--card)', maxWidth: '800px', margin: '2rem auto' }}>
      <div className="player-image" style={{
        width: '115px',
        height: '115px',
        borderRadius: '50%',
        background: 'var(--primary)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '48px',
        fontWeight: 'bold',
        color: 'var(--primary-foreground)',
        marginRight: '16px',
        flexShrink: 0
      }}>
        {user.first_name.charAt(0)}{user.last_name.charAt(0)}
      </div>
      <div className="player-details">
        <h2 className="player-name">{user.first_name} {user.last_name}</h2>
        <p className="player-club">{user.email}</p>
        <div className="player-meta">
          <p><strong>Age:</strong> {user.age}</p>
          <p><strong>Gender:</strong> {user.gender}</p>
          {!loading && (
            <>
              <p><strong>Matches:</strong> {stats.totalMatches}</p>
              <p><strong>Goals:</strong> {stats.totalGoals}</p>
              <p><strong>Assists:</strong> {stats.totalAssists}</p>
              {stats.totalMatches > 0 && (
                <p><strong>Avg Rating:</strong> {stats.averageRating.toFixed(2)}</p>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default PlayerInfoCard;
