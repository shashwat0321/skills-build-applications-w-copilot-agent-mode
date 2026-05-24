import React, { useEffect, useState } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/workouts/`
    : 'http://localhost:8000/api/workouts/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setWorkouts(results);
        console.log('Fetched workouts:', results);
        console.log('Endpoint used:', endpoint);
      });
  }, [endpoint]);

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h2 className="mb-0">Workouts</h2>
        <button className="btn btn-warning btn-sm">Add Workout</button>
      </div>
      <div className="card-body">
        <table className="table table-hover table-bordered">
          <thead className="table-light">
            <tr>
              <th>Name</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            {workouts.map((workout, idx) => (
              <tr key={idx}>
                <td>{workout.name}</td>
                <td>{workout.duration}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Workouts;
