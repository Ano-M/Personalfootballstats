import React, { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";
import type { MatchStats, LeaderboardEntry, MatchDetail } from "../types";
import api from "../services/api";
import "../styles/dark-theme.css";

const PlayerTabs: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState<"stats" | "add">("stats");
  const [formValues, setFormValues] = useState<MatchStats>({
    date: new Date().toISOString().split('T')[0],
    home_team: "",
    away_team: "",
    match_score: "",
    minutes_played: 90,
    goals: 0,
    shots: 0,
    disallowed_goals: 0,
    assists: 0,
    passes: 0,
    successful_passes: 0,
    dribbles: 0,
    successful_dribbles: 0,
    tackles: 0,
    missed_tackles: 0,
    interceptions: 0,
    touches: 0,
    unsuccessful_touches: 0,
  });

  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [selectedMatch, setSelectedMatch] = useState<MatchDetail | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Fetch leaderboard when stats tab is active
  useEffect(() => {
    if (activeTab === "stats" && isAuthenticated) {
      fetchLeaderboard();
    }
  }, [activeTab, isAuthenticated]);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const data = await api.stats.getLeaderboard();
      setLeaderboard(data);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load leaderboard");
    } finally {
      setLoading(false);
    }
  };

  const fetchMatchDetail = async (matchId: number) => {
    try {
      setLoading(true);
      const data = await api.stats.getMatch(matchId);
      setSelectedMatch(data);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load match details");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value, type } = event.target;
    setFormValues((prev) => ({
      ...prev,
      [id]: type === "number" ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    // Validation
    if (!formValues.home_team || !formValues.away_team || !formValues.match_score) {
      setError("Please fill in all match information fields");
      setLoading(false);
      return;
    }

    try {
      const response = await api.stats.submit(formValues);
      setSuccess(`Match stats saved successfully! Match ID: ${response.match_id}`);

      // Reset form
      setFormValues({
        date: new Date().toISOString().split('T')[0],
        home_team: "",
        away_team: "",
        match_score: "",
        minutes_played: 90,
        goals: 0,
        shots: 0,
        disallowed_goals: 0,
        assists: 0,
        passes: 0,
        successful_passes: 0,
        dribbles: 0,
        successful_dribbles: 0,
        tackles: 0,
        missed_tackles: 0,
        interceptions: 0,
        touches: 0,
        unsuccessful_touches: 0,
      });

      // Switch to stats tab after successful submission
      setTimeout(() => {
        setActiveTab("stats");
        setSuccess("");
      }, 2000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit stats");
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="player-tabs dark">
        <div style={{ textAlign: 'center', padding: '2rem' }}>
          <h3>Please log in to access match statistics</h3>
        </div>
      </div>
    );
  }

  return (
    <div className="player-tabs dark">
      {/* Tab buttons */}
      <div className="tab-buttons">
        <button
          className={activeTab === "stats" ? "active" : ""}
          onClick={() => setActiveTab("stats")}
        >
          Stats
        </button>
        <button
          className={activeTab === "add" ? "active" : ""}
          onClick={() => setActiveTab("add")}
        >
          Add Match
        </button>
      </div>

      <div className="tab-content">
        {/* Stats Tab - Leaderboard */}
        {activeTab === "stats" && (
          <div className="stats-tab">
            <h2>Personal Leaderboard</h2>

            {loading && <p>Loading...</p>}
            {error && <div className="error-message">{error}</div>}

            {!loading && !selectedMatch && leaderboard.length === 0 && (
              <p>No matches recorded yet. Add your first match!</p>
            )}

            {!loading && !selectedMatch && leaderboard.length > 0 && (
              <div className="leaderboard-table">
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Date</th>
                      <th>Match</th>
                      <th>Score</th>
                      <th>Goals</th>
                      <th>Assists</th>
                      <th>Minutes</th>
                      <th>Rating</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaderboard.map((entry, index) => (
                      <tr key={entry.match_id}>
                        <td>{index + 1}</td>
                        <td>{entry.date}</td>
                        <td>{entry.match}</td>
                        <td>{entry.score}</td>
                        <td>{entry.goals}</td>
                        <td>{entry.assists}</td>
                        <td>{entry.minutes}</td>
                        <td><strong>{entry.rating.toFixed(1)}</strong></td>
                        <td>
                          <button
                            onClick={() => fetchMatchDetail(entry.match_id)}
                            style={{
                              padding: '4px 8px',
                              cursor: 'pointer',
                              background: 'var(--primary)',
                              color: 'var(--primary-foreground)',
                              border: 'none',
                              borderRadius: '4px'
                            }}
                          >
                            View
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {/* Match Detail View */}
            {selectedMatch && (
              <div className="match-detail">
                <button
                  onClick={() => setSelectedMatch(null)}
                  style={{
                    marginBottom: '1rem',
                    padding: '8px 16px',
                    cursor: 'pointer',
                    background: 'var(--border)',
                    color: 'var(--foreground)',
                    border: 'none',
                    borderRadius: '4px'
                  }}
                >
                  ← Back to Leaderboard
                </button>

                <h2>Match Details - ID: {selectedMatch.match_id}</h2>
                <div style={{ marginBottom: '1rem' }}>
                  <p><strong>Date:</strong> {selectedMatch.date}</p>
                  <p><strong>Match:</strong> {selectedMatch.home_team} vs {selectedMatch.away_team}</p>
                  <p><strong>Score:</strong> {selectedMatch.match_score}</p>
                  <p><strong>Minutes Played:</strong> {selectedMatch.minutes_played}</p>
                  <p><strong>Performance Rating:</strong> {selectedMatch.rating.toFixed(1)}/10</p>
                </div>

                <hr />

                <div className="stats-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
                  <div>
                    <h3>Attacking</h3>
                    <p>Goals: {selectedMatch.goals}</p>
                    <p>Shots: {selectedMatch.shots}</p>
                    <p>Disallowed Goals: {selectedMatch.disallowed_goals}</p>
                    <p>Assists: {selectedMatch.assists}</p>
                    <p>Goal Involvements: {selectedMatch.goal_involvements}</p>
                  </div>

                  <div>
                    <h3>Passing</h3>
                    <p>Passes: {selectedMatch.successful_passes}/{selectedMatch.passes}</p>
                    <p>Accuracy: {selectedMatch.passes > 0 ? ((selectedMatch.successful_passes / selectedMatch.passes) * 100).toFixed(1) : 0}%</p>
                  </div>

                  <div>
                    <h3>Dribbling</h3>
                    <p>Dribbles: {selectedMatch.successful_dribbles}/{selectedMatch.dribbles}</p>
                    <p>Success Rate: {selectedMatch.dribbles > 0 ? ((selectedMatch.successful_dribbles / selectedMatch.dribbles) * 100).toFixed(1) : 0}%</p>
                  </div>

                  <div>
                    <h3>Defensive</h3>
                    <p>Tackles: {selectedMatch.tackles}</p>
                    <p>Missed Tackles: {selectedMatch.missed_tackles}</p>
                    <p>Interceptions: {selectedMatch.interceptions}</p>
                  </div>

                  <div>
                    <h3>Ball Control</h3>
                    <p>Touches: {selectedMatch.touches - selectedMatch.unsuccessful_touches}/{selectedMatch.touches}</p>
                    <p>Success Rate: {selectedMatch.touches > 0 ? (((selectedMatch.touches - selectedMatch.unsuccessful_touches) / selectedMatch.touches) * 100).toFixed(1) : 0}%</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Add Match Tab */}
        {activeTab === "add" && (
          <div className="add-match-tab">
            <h2>Add Match Statistics</h2>
            <form onSubmit={handleSubmit}>
              {/* Match Info */}
              <div className="form-section">
                <h3>Match Information</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="date">Date *</label>
                    <input
                      id="date"
                      type="date"
                      value={formValues.date}
                      onChange={handleInputChange}
                      required
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="minutes_played">Minutes Played (1-120) *</label>
                    <input
                      id="minutes_played"
                      type="number"
                      min="1"
                      max="120"
                      value={formValues.minutes_played}
                      onChange={handleInputChange}
                      required
                      disabled={loading}
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="home_team">Home Team *</label>
                    <input
                      id="home_team"
                      type="text"
                      value={formValues.home_team}
                      onChange={handleInputChange}
                      placeholder="e.g., Manchester United"
                      required
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="away_team">Away Team *</label>
                    <input
                      id="away_team"
                      type="text"
                      value={formValues.away_team}
                      onChange={handleInputChange}
                      placeholder="e.g., Liverpool"
                      required
                      disabled={loading}
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="match_score">Match Score (X-Y) *</label>
                    <input
                      id="match_score"
                      type="text"
                      value={formValues.match_score}
                      onChange={handleInputChange}
                      placeholder="e.g., 2-1"
                      required
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>

              <hr />

              {/* Attacking Stats */}
              <div className="form-section">
                <h3>Attacking Statistics</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="goals">Goals (0-15)</label>
                    <input
                      id="goals"
                      type="number"
                      min="0"
                      max="15"
                      value={formValues.goals}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="shots">Shots (0-30)</label>
                    <input
                      id="shots"
                      type="number"
                      min="0"
                      max="30"
                      value={formValues.shots}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="disallowed_goals">Disallowed Goals (0-5)</label>
                    <input
                      id="disallowed_goals"
                      type="number"
                      min="0"
                      max="5"
                      value={formValues.disallowed_goals}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="assists">Assists (0-15)</label>
                    <input
                      id="assists"
                      type="number"
                      min="0"
                      max="15"
                      value={formValues.assists}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>

              <hr />

              {/* Passing Stats */}
              <div className="form-section">
                <h3>Passing Statistics</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="passes">Total Passes (0-200)</label>
                    <input
                      id="passes"
                      type="number"
                      min="0"
                      max="200"
                      value={formValues.passes}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="successful_passes">Successful Passes (0-200)</label>
                    <input
                      id="successful_passes"
                      type="number"
                      min="0"
                      max="200"
                      value={formValues.successful_passes}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>

              <hr />

              {/* Dribbling Stats */}
              <div className="form-section">
                <h3>Dribbling Statistics</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="dribbles">Total Dribbles (0-50)</label>
                    <input
                      id="dribbles"
                      type="number"
                      min="0"
                      max="50"
                      value={formValues.dribbles}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="successful_dribbles">Successful Dribbles (0-50)</label>
                    <input
                      id="successful_dribbles"
                      type="number"
                      min="0"
                      max="50"
                      value={formValues.successful_dribbles}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>

              <hr />

              {/* Defensive Stats */}
              <div className="form-section">
                <h3>Defensive Statistics</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="tackles">Tackles (0-30)</label>
                    <input
                      id="tackles"
                      type="number"
                      min="0"
                      max="30"
                      value={formValues.tackles}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="missed_tackles">Missed Tackles (0-30)</label>
                    <input
                      id="missed_tackles"
                      type="number"
                      min="0"
                      max="30"
                      value={formValues.missed_tackles}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="interceptions">Interceptions (0-30)</label>
                    <input
                      id="interceptions"
                      type="number"
                      min="0"
                      max="30"
                      value={formValues.interceptions}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>

              <hr />

              {/* Ball Control Stats */}
              <div className="form-section">
                <h3>Ball Control</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="touches">Total Touches (0-300)</label>
                    <input
                      id="touches"
                      type="number"
                      min="0"
                      max="300"
                      value={formValues.touches}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="unsuccessful_touches">Unsuccessful Touches (0-300)</label>
                    <input
                      id="unsuccessful_touches"
                      type="number"
                      min="0"
                      max="300"
                      value={formValues.unsuccessful_touches}
                      onChange={handleInputChange}
                      disabled={loading}
                    />
                  </div>
                </div>
              </div>

              {error && <div className="error-message">{error}</div>}
              {success && <div className="success-message">{success}</div>}

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? "Submitting..." : "Submit Match Statistics"}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlayerTabs;
