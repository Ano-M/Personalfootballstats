import React, { useState } from "react";
import "../styles/dark-theme.css";

interface MatchStats {
  teams: string;
  score: string;
  goals: number;
  assists: number;
  shots: number;
  disallowed: number;
  goalInvolvements: number;
  dribbles: number;
  successfulDribbles: number;
  passes: number;
  successfulPasses: number;
  touches: number;
  unsuccessfulTouches: number;
  tackles: number;
  missedTackles: number;
  interceptions: number;
}

const PlayerTabs: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"stats" | "add">("stats");
  const [formValues, setFormValues] = useState<MatchStats>({
    teams: "",
    score: "",
    goals: 0,
    assists: 0,
    shots: 0,
    disallowed: 0,
    goalInvolvements: 0,
    dribbles: 0,
    successfulDribbles: 0,
    passes: 0,
    successfulPasses: 0,
    touches: 0,
    unsuccessfulTouches: 0,
    tackles: 0,
    missedTackles: 0,
    interceptions: 0,
  });

  // Handle input changes for controlled components
  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value, type } = event.target;
    setFormValues((prev) => ({
      ...prev,
      [id]: type === "number" ? Number(value) : value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    fetch(import.meta.env.REACT_APP_API_SAVE_STATS || 'http://127.0.0.1:5000/api/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' 
      },
      body: JSON.stringify(formValues)
    })
      .then(response => response.json())
      .then(data => console.log('Saved stats:', data))
      .catch(error => console.error('Error:', error));
  };

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
        {activeTab === "stats" && (
          <div className="stats-tab">
            <h3>Leaderboard</h3>
            <p>Stats go here...</p>
          </div>
        )}

        {activeTab === "add" && (
          <div className="add-match-tab">
            <h2>Add Match Statistics to calculate rating</h2>
            <form onSubmit={handleSubmit}>
              {/* Match Info */}
              <div className="form-section">
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="teams">Teams</label>
                    <input id="teams" type="text" value={formValues.teams} onChange={handleInputChange} placeholder="e.g., Team A vs Team B" />
                  </div>
                  <div className="form-group">
                    <label htmlFor="score">Score</label>
                    <input id="score" type="text" value={formValues.score} onChange={handleInputChange} placeholder="e.g., 2-1" />
                  </div>
                </div>
              </div>

              <hr />

              {/* Attacking Stats */}
              <div className="form-section">
                <h3>Attacking Statistics</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="goals">Goals</label>
                    <input id="goals" type="number" min="0" value={formValues.goals} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="assists">Assists</label>
                    <input id="assists" type="number" min="0" value={formValues.assists} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="shots">Shots</label>
                    <input id="shots" type="number" min="0" value={formValues.shots} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="disallowed">Disallowed Goals</label>
                    <input id="disallowed" type="number" min="0" value={formValues.disallowed} onChange={handleInputChange} />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="goalInvolvements">Goal Involvements</label>
                    <input id="goalInvolvements" type="number" min="0" value={formValues.goalInvolvements} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="dribbles">Dribbles</label>
                    <input id="dribbles" type="number" min="0" value={formValues.dribbles} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="successfulDribbles">Successful Dribbles</label>
                    <input id="successfulDribbles" type="number" min="0" value={formValues.successfulDribbles} onChange={handleInputChange} />
                  </div>
                </div>
              </div>

              <hr />

              {/* Passing & Possession */}
              <div className="form-section">
                <h3>Passing & Possession</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="passes">Passes</label>
                    <input id="passes" type="number" min="0" value={formValues.passes} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="successfulPasses">Successful Passes</label>
                    <input id="successfulPasses" type="number" min="0" value={formValues.successfulPasses} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="touches">Touches</label>
                    <input id="touches" type="number" min="0" value={formValues.touches} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="unsuccessfulTouches">Unsuccessful Touches</label>
                    <input id="unsuccessfulTouches" type="number" min="0" value={formValues.unsuccessfulTouches} onChange={handleInputChange} />
                  </div>
                </div>
              </div>

              <hr />

              {/* Defensive Stats */}
              <div className="form-section">
                <h3>Defensive Statistics</h3>
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="tackles">Tackles</label>
                    <input id="tackles" type="number" min="0" value={formValues.tackles} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="missedTackles">Missed Tackles</label>
                    <input id="missedTackles" type="number" min="0" value={formValues.missedTackles} onChange={handleInputChange} />
                  </div>
                  <div className="form-group">
                    <label htmlFor="interceptions">Interceptions</label>
                    <input id="interceptions" type="number" min="0" value={formValues.interceptions} onChange={handleInputChange} />
                  </div>
                </div>
              </div>
              <button type="submit" className="submit-btn">
                Submit Match Statistics
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlayerTabs;
