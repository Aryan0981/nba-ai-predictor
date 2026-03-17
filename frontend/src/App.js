import React, { useState } from "react";

const teamPlayers = {
  "Lakers": ["LeBron James", "Luka Doncic", "Austin Reaves"],
  "Nuggets": ["Nikola Jokic", "Jamal Murray", "Christian Braun"],
  "Heat": ["Bam Adebayo", "Tyler Herro", "Jimmy Butler"],
  "Hornets": ["LaMelo Ball", "Miles Bridges", "Brandon Miller"],
  "Magic": ["Paolo Banchero", "Franz Wagner", "Jalen Suggs"],
  "Thunder": ["Shai Gilgeous-Alexander", "Jalen Williams", "Chet Holmgren"],
  "Wizards": ["Jordan Poole", "Kyle Kuzma", "Bilal Coulibaly"],
  "Pistons": ["Cade Cunningham", "Jaden Ivey", "Jalen Duren"],
  "Pacers": ["Tyrese Haliburton", "Pascal Siakam", "Myles Turner"],
  "Knicks": ["Jalen Brunson", "Julius Randle", "OG Anunoby"],
  "Cavaliers": ["Donovan Mitchell", "Darius Garland", "Evan Mobley"],
  "Bucks": ["Giannis Antetokounmpo", "Damian Lillard", "Khris Middleton"],
  "Suns": ["Kevin Durant", "Devin Booker", "Bradley Beal"],
  "Timberwolves": ["Anthony Edwards", "Karl-Anthony Towns", "Rudy Gobert"],
  "76ers": ["Joel Embiid", "Tyrese Maxey", "Paul George"],
  "Kings": ["De'Aaron Fox", "Domantas Sabonis", "Keegan Murray"],
  "Spurs": ["Victor Wembanyama", "Devin Vassell", "Keldon Johnson"]
};

function App() {
  const [games, setGames] = useState([]);
  const [summary, setSummary] = useState(null);

  const loadGames = async () => {
    const res = await fetch("http://127.0.0.1:8000/games-today");
    const data = await res.json();
    setGames(data);
  };

  const loadSummary = async (homeTeam, awayTeam) => {
  console.log("homeTeam:", homeTeam);
  console.log("awayTeam:", awayTeam);

  const team1Players = teamPlayers[homeTeam];
  const team2Players = teamPlayers[awayTeam];

  if (!team1Players || !team2Players) {
    alert("Player mapping not added yet for one of these teams.");
    return;
  }

  const url =
    `http://127.0.0.1:8000/game-summary?team1=${encodeURIComponent(homeTeam)}` +
    `&team2=${encodeURIComponent(awayTeam)}` +
    `&team1_players=${encodeURIComponent(team1Players.join(", "))}` +
    `&team2_players=${encodeURIComponent(team2Players.join(", "))}`;

  const res = await fetch(url);
  const data = await res.json();
  setSummary(data);
};

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>NBA AI Predictor</h1>

      <button onClick={loadGames}>Load Today's Games</button>

      <h2>Today's Games</h2>
      <ul>
        {games.map((game) => (
          <li key={game.game_id}>
            {game.away_team} @ {game.home_team}{" "}
            <button onClick={() => loadSummary(game.home_team, game.away_team)}>
              Predict Game
            </button>
          </li>
        ))}
      </ul>

      {summary && (
        <div style={{ marginTop: "20px" }}>
          <h2>
            {summary.matchup.team2} @ {summary.matchup.team1}
          </h2>

          <p>
            <strong>Winner:</strong> {summary.prediction.predicted_winner}
          </p>
          <p>
            <strong>Confidence:</strong> {summary.prediction.confidence}%
          </p>

          <p><strong>Projected Scores:</strong></p>
          <pre>{JSON.stringify(summary.prediction.projected_scores, null, 2)}</pre>

          <p><strong>Reasons:</strong></p>
          <ul>
            {summary.prediction.reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>

          <h3>{summary.matchup.team1} Players</h3>
          <ul>
            {summary.players[summary.matchup.team1].map((player, index) => (
              <li key={index}>
                {player.player}: {player.projected_points_range[0]} - {player.projected_points_range[1]} pts
              </li>
            ))}
          </ul>

          <h3>{summary.matchup.team2} Players</h3>
          <ul>
            {summary.players[summary.matchup.team2].map((player, index) => (
              <li key={index}>
                {player.player}: {player.projected_points_range[0]} - {player.projected_points_range[1]} pts
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;