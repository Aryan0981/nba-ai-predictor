import React, { useState } from "react";
import "./App.css";

const teamPlayers = {
  "Atlanta Hawks": ["Trae Young", "Jalen Johnson", "Clint Capela"],
  "Boston Celtics": ["Jayson Tatum", "Jaylen Brown", "Kristaps Porzingis"],
  "Brooklyn Nets": ["Mikal Bridges", "Cam Thomas", "Nic Claxton"],
  "Charlotte Hornets": ["LaMelo Ball", "Miles Bridges", "Brandon Miller"],
  "Chicago Bulls": ["Zach LaVine", "DeMar DeRozan", "Nikola Vucevic"],
  "Cleveland Cavaliers": ["Donovan Mitchell", "Darius Garland", "Evan Mobley"],
  "Dallas Mavericks": ["Luka Doncic", "Kyrie Irving", "Klay Thompson"],
  "Denver Nuggets": ["Nikola Jokic", "Jamal Murray", "Michael Porter Jr."],
  "Detroit Pistons": ["Cade Cunningham", "Jaden Ivey", "Jalen Duren"],
  "Golden State Warriors": ["Stephen Curry", "Draymond Green", "Jonathan Kuminga"],
  "Houston Rockets": ["Jalen Green", "Alperen Sengun", "Fred VanVleet"],
  "Indiana Pacers": ["Tyrese Haliburton", "Pascal Siakam", "Myles Turner"],
  "Los Angeles Clippers": ["Kawhi Leonard", "James Harden", "Paul George"],
  "Los Angeles Lakers": ["LeBron James", "Luka Doncic", "Austin Reaves"],
  "Memphis Grizzlies": ["Ja Morant", "Desmond Bane", "Jaren Jackson Jr."],
  "Miami Heat": ["Bam Adebayo", "Tyler Herro", "Jimmy Butler"],
  "Milwaukee Bucks": ["Giannis Antetokounmpo", "Damian Lillard", "Khris Middleton"],
  "Minnesota Timberwolves": ["Anthony Edwards", "Julius Randle", "Rudy Gobert"],
  "New Orleans Pelicans": ["Zion Williamson", "Brandon Ingram", "CJ McCollum"],
  "New York Knicks": ["Jalen Brunson", "OG Anunoby", "Karl-Anthony Towns"],
  "Oklahoma City Thunder": ["Shai Gilgeous-Alexander", "Jalen Williams", "Chet Holmgren"],
  "Orlando Magic": ["Paolo Banchero", "Franz Wagner", "Jalen Suggs"],
  "Philadelphia 76ers": ["Joel Embiid", "Tyrese Maxey", "Paul George"],
  "Phoenix Suns": ["Kevin Durant", "Devin Booker", "Bradley Beal"],
  "Portland Trail Blazers": ["Anfernee Simons", "Jerami Grant", "Deandre Ayton"],
  "Sacramento Kings": ["De'Aaron Fox", "Domantas Sabonis", "Keegan Murray"],
  "San Antonio Spurs": ["Victor Wembanyama", "Devin Vassell", "Keldon Johnson"],
  "Toronto Raptors": ["Scottie Barnes", "RJ Barrett", "Immanuel Quickley"],
  "Utah Jazz": ["Lauri Markkanen", "Collin Sexton", "Jordan Clarkson"],
  "Washington Wizards": ["Jordan Poole", "Kyle Kuzma", "Bilal Coulibaly"],
};

const teamNameAliases = {
  Hawks: "Atlanta Hawks",
  Celtics: "Boston Celtics",
  Nets: "Brooklyn Nets",
  Hornets: "Charlotte Hornets",
  Bulls: "Chicago Bulls",
  Cavaliers: "Cleveland Cavaliers",
  Cavs: "Cleveland Cavaliers",
  Mavericks: "Dallas Mavericks",
  Mavs: "Dallas Mavericks",
  Nuggets: "Denver Nuggets",
  Pistons: "Detroit Pistons",
  Warriors: "Golden State Warriors",
  Rockets: "Houston Rockets",
  Pacers: "Indiana Pacers",
  Clippers: "Los Angeles Clippers",
  "LA Clippers": "Los Angeles Clippers",
  Lakers: "Los Angeles Lakers",
  "LA Lakers": "Los Angeles Lakers",
  Grizzlies: "Memphis Grizzlies",
  Heat: "Miami Heat",
  Bucks: "Milwaukee Bucks",
  Timberwolves: "Minnesota Timberwolves",
  Wolves: "Minnesota Timberwolves",
  Pelicans: "New Orleans Pelicans",
  Knicks: "New York Knicks",
  Thunder: "Oklahoma City Thunder",
  Magic: "Orlando Magic",
  "76ers": "Philadelphia 76ers",
  Sixers: "Philadelphia 76ers",
  Suns: "Phoenix Suns",
  "Trail Blazers": "Portland Trail Blazers",
  Blazers: "Portland Trail Blazers",
  Kings: "Sacramento Kings",
  Spurs: "San Antonio Spurs",
  Raptors: "Toronto Raptors",
  Jazz: "Utah Jazz",
  Wizards: "Washington Wizards",
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
    const normalizedHomeTeam = teamNameAliases[homeTeam] || homeTeam;
    const normalizedAwayTeam = teamNameAliases[awayTeam] || awayTeam;

    const team1Players = teamPlayers[normalizedHomeTeam];
    const team2Players = teamPlayers[normalizedAwayTeam];

    if (!team1Players || !team2Players) {
      console.log("Original homeTeam:", homeTeam);
      console.log("Original awayTeam:", awayTeam);
      console.log("Normalized homeTeam:", normalizedHomeTeam);
      console.log("Normalized awayTeam:", normalizedAwayTeam);
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

  const clearPrediction = () => {
      setSummary(null);
      setSelectedGame("");
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
                className={`game-row ${
                  selectedGame === `${game.away_team} @ ${game.home_team}`
                    ? "selected-game-row"
                    : ""
                }`}
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

        {summary && (
          <button className="clear-button" onClick={clearPrediction}>
            Clear Prediction
          </button>
        )}

        {!summary && !loadingSummary && (
          <p>Select a game to see the prediction.</p>
        )}

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
              <div className="score-grid">
                {Object.entries(summary.prediction.projected_scores).map(
                  ([team, range]) => (
                    <div className="score-card" key={team}>
                      <p className="score-team">{team}</p>
                      <p className="score-range">
                        {range[0]} - {range[1]}
                      </p>
                    </div>
                  )
                )}
              </div>
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
              <div className="player-card">
                <h4>{summary.matchup.team1} Players</h4>
                <div className="player-list">
                  {summary.players[summary.matchup.team1].map((player, index) => (
                    <div className="player-row" key={index}>
                      <span className="player-name">{player.player}</span>
                      <span className="player-range">
                        {player.projected_points_range[0]} -{" "}
                        {player.projected_points_range[1]} pts
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="player-card">
                <h4>{summary.matchup.team2} Players</h4>
                <div className="player-list">
                  {summary.players[summary.matchup.team2].map((player, index) => (
                    <div className="player-row" key={index}>
                      <span className="player-name">{player.player}</span>
                      <span className="player-range">
                        {player.projected_points_range[0]} -{" "}
                        {player.projected_points_range[1]} pts
                      </span>
                    </div>
                  ))}
                </div>
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