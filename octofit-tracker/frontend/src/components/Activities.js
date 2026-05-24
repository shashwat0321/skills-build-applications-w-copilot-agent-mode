import React, { useEffect, useState } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const endpoint = codespace
    ? `https://${codespace}-8000.app.github.dev/api/activities/`
    : 'http://localhost:8000/api/activities/';

  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setActivities(results);
        console.log('Fetched activities:', results);
        console.log('Endpoint used:', endpoint);
      });
  }, [endpoint]);

  return (
    <div className="card shadow-sm mb-4">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h2 className="mb-0">Activities</h2>
        <button className="btn btn-success btn-sm">Add Activity</button>
      </div>
      <div className="card-body">
        <table className="table table-hover table-bordered">
          <thead className="table-light">
            <tr>
              <th>Name</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity, idx) => (
              <tr key={idx}>
                <td>{activity.name}</td>
                <td>{activity.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Activities;
