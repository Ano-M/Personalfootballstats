import React, { useState } from "react";
import "../styles/dark-theme.css";

const PlayerTabs: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"stats" | "add">("stats");

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

            {/* Match Info */}
            <div className="form-section">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="teams">Teams</label>
                  <input id="teams" type="text" placeholder="e.g., Team A vs Team B" />
                </div>
                <div className="form-group">
                  <label htmlFor="score">Score</label>
                  <input id="score" type="text" placeholder="e.g., 2-1" />
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
                  <input id="goals" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="assists">Assists</label>
                  <input id="assists" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="shots">Shots</label>
                  <input id="shots" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="disallowed">Disallowed Goals</label>
                  <input id="disallowed" type="number" min="0" />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="goalInvolvements">Goal Involvements</label>
                  <input id="goalInvolvements" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="dribbles">Dribbles</label>
                  <input id="dribbles" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="successfulDribbles">Successful Dribbles</label>
                  <input id="successfulDribbles" type="number" min="0" />
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
                  <input id="passes" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="successfulPasses">Successful Passes</label>
                  <input id="successfulPasses" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="touches">Touches</label>
                  <input id="touches" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="unsuccessfulTouches">Unsuccessful Touches</label>
                  <input id="unsuccessfulTouches" type="number" min="0" />
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
                  <input id="tackles" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="missedTackles">Missed Tackles</label>
                  <input id="missedTackles" type="number" min="0" />
                </div>
                <div className="form-group">
                  <label htmlFor="interceptions">Interceptions</label>
                  <input id="interceptions" type="number" min="0" />
                </div>
              </div>
            </div>

            <button type="submit" className="submit-btn">
              Submit Match Statistics
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default PlayerTabs;
