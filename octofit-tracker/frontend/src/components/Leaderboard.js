import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/leaderboard/`
    : 'http://localhost:8000/api/leaderboard/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setLeaderboard(results);
        console.log('Fetched leaderboard:', results);
        console.log('Endpoint used:', endpoint);
      });
  }, [endpoint]);

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h2 className="mb-0">Leaderboard</h2>
        <button className="btn btn-info btn-sm">Refresh</button>
      </div>
      <div className="card-body">
        <table className="table table-hover table-bordered">
          <thead className="table-light">
            <tr>
              <th>User</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, idx) => (
              <tr key={idx}>
                <td>{entry.user}</td>
                <td>{entry.score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;
