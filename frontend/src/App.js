import React, { useState } from "react";
import "./App.css";

const teamPlayers = {
  Lakers: ["LeBron James", "Luka Doncic", "Austin Reaves"],
  Nuggets: ["Nikola Jokic", "Jamal Murray", "Christian Braun"],
  Heat: ["Bam Adebayo", "Tyler Herro", "Jimmy Butler"],
  Hornets: ["LaMelo Ball", "Miles Bridges", "Brandon Miller"],
  Magic: ["Paolo Banchero", "Franz Wagner", "Jalen Suggs"],
  Thunder: ["Shai Gilgeous-Alexander", "Jalen Williams", "Chet Holmgren"],
  Wizards: ["Jordan Poole", "Kyle Kuzma", "Bilal Coulibaly"],
  Pistons: ["Cade Cunningham", "Jaden Ivey", "Jalen Duren"],
  Pacers: ["Tyrese Haliburton", "Pascal Siakam", "Myles Turner"],
  Knicks: ["Jalen Brunson", "OG Anunoby", "Karl-Anthony Towns"],
  Cavaliers: ["Donovan Mitchell", "Darius Garland", "Evan Mobley"],
  Bucks: ["Giannis Antetokounmpo", "Damian Lillard", "Khris Middleton"],
  Suns: ["Kevin Durant", "Devin Booker", "Bradley Beal"],
  Timberwolves: ["Anthony Edwards", "Julius Randle", "Rudy Gobert"],
  "76ers": ["Joel Embiid", "Tyrese Maxey", "Paul George"],
  Spurs: ["Victor Wembanyama", "Devin Vassell", "Keldon Johnson"],
  Kings: ["De'Aaron Fox", "Domantas Sabonis", "Keegan Murray"],
};

function App() {
  const [games, setGames] = useState([]);
  const [summary, setSummary] = useState(null);
  const [selectedGame, setSelectedGame] = useState("");
  const [loadingGames, setLoadingGames] = useState(false);
  const [loadingSummary, setLoadingSummary] = useState(false);

  const loadGames = async () => {
    setLoadingGames(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/games-today");
      const data = await res.json();
      setGames(data);
    } catch (error) {
      alert("Could not load today's games.");
      console.error(error);
    } finally {
      setLoadingGames(false);
    }
  };

  const loadSummary = async (homeTeam, awayTeam) => {
    const team1Players = teamPlayers[homeTeam];
    const team2Players = teamPlayers[awayTeam];

    if (!team1Players || !team2Players) {
      alert("Player mapping not added yet for one of these teams.");
      return;
    }

    setSelectedGame(`${awayTeam} @ ${homeTeam}`);
    setLoadingSummary(true);

    try {
      const url =
        `http://127.0.0.1:8000/game-summary?team1=${encodeURIComponent(homeTeam)}` +
        `&team2=${encodeURIComponent(awayTeam)}` +
        `&team1_players=${encodeURIComponent(team1Players.join(", "))}` +
        `&team2_players=${encodeURIComponent(team2Players.join(", "))}`;

      const res = await fetch(url);
      const data = await res.json();
      setSummary(data);
    } catch (error) {
      alert("Could not load game summary.");
      console.error(error);
    } finally {
      setLoadingSummary(false);
    }
  };


  return (
  <div className="app-container">
    <h1 className="app-title">NBA AI Predictor</h1>
    <p className="app-subtitle">
      Live game matchups, winner predictions, score ranges, and player projections.
    </p>

    <button className="load-button" onClick={loadGames}>
      {loadingGames ? "Loading..." : "Load Today's Games"}
    </button>

    <div className="dashboard-grid">
      <div className="card">
        <h2 className="section-title">Today's Games</h2>
        {games.length === 0 ? (
          <p>No games loaded yet.</p>
        ) : (
          <div className="game-list">
            {games.map((game) => (
              <div
                className={`game-row ${selectedGame === `${game.away_team} @ ${game.home_team}` ? "selected-game-row" : ""}`}
                key={game.game_id}
              >
                <div>
                  <strong>
                    {game.away_team} @ {game.home_team}
                  </strong>
                </div>
                <button
                  className="predict-button"
                  onClick={() => loadSummary(game.home_team, game.away_team)}
                >
                  Predict
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="card">
        <h2 className="section-title">Prediction Dashboard</h2>

        {!summary && !loadingSummary && <p>Select a game to see the prediction.</p>}
        {loadingSummary && <p>Loading prediction...</p>}

        {summary && !loadingSummary && (
          <div>
            <h3 className="selected-game-title">{selectedGame}</h3>

            <div className="summary-block">
              <p>
                <strong>Winner:</strong> {summary.prediction.predicted_winner}
              </p>
              <p>
                <strong>Confidence:</strong> {summary.prediction.confidence}%
              </p>
            </div>

            <div className="summary-block">
              <h4>Projected Scores</h4>
              {Object.entries(summary.prediction.projected_scores).map(([team, range]) => (
                <p key={team}>
                  <strong>{team}:</strong> {range[0]} - {range[1]}
                </p>
              ))}
            </div>

            <div className="summary-block">
              <h4>Reasons</h4>
              <ul>
                {summary.prediction.reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </div>

            <div className="player-grid">
              <div>
                <h4>{summary.matchup.team1} Players</h4>
                <ul>
                  {summary.players[summary.matchup.team1].map((player, index) => (
                    <li key={index}>
                      {player.player}: {player.projected_points_range[0]} -{" "}
                      {player.projected_points_range[1]} pts
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h4>{summary.matchup.team2} Players</h4>
                <ul>
                  {summary.players[summary.matchup.team2].map((player, index) => (
                    <li key={index}>
                      {player.player}: {player.projected_points_range[0]} -{" "}
                      {player.projected_points_range[1]} pts
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
);
}

export default App;