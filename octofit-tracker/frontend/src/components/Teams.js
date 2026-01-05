import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalData, setModalData] = useState(null);
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  const baseUrl = codespace ? `https://${codespace}-8000.app.github.dev/api` : `${window.location.origin}/api`;
  const endpoint = `${baseUrl}/teams/`;

  const fetchData = () => {
    setLoading(true);
    console.log('[Teams] endpoint:', endpoint);
    fetch(endpoint)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        console.log('[Teams] response:', json);
        const items = Array.isArray(json) ? json : (json && Array.isArray(json.results) ? json.results : []);
        setData(items);
      })
      .catch((err) => console.error('[Teams] fetch error:', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, [endpoint]);

  const headers = data.length ? Object.keys(data[0]) : [];

  return (
    <div className="card">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h2 className="h5 mb-0">Teams</h2>
        <button className="btn btn-sm btn-primary" onClick={fetchData}>Refresh</button>
      </div>
      <div className="card-body">
        {loading ? (
          <div>Loading…</div>
        ) : data.length ? (
          <div className="table-responsive">
            <table className="table table-striped table-hover table-sm">
              <thead>
                <tr>
                  {headers.map((h) => (
                    <th key={h}>{h}</th>
                  ))}
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {data.map((row, idx) => (
                  <tr key={idx}>
                    {headers.map((k) => (
                      <td key={k}>{typeof row[k] === 'object' ? JSON.stringify(row[k]) : String(row[k])}</td>
                    ))}
                    <td>
                      <button className="btn btn-xs btn-outline-primary" onClick={() => setModalData(row)}>View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-muted">No teams available.</p>
        )}

        {modalData && (
          <div className="modal d-block" tabIndex="-1" role="dialog">
            <div className="modal-dialog modal-lg" role="document">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Team detail</h5>
                  <button type="button" className="btn-close" aria-label="Close" onClick={() => setModalData(null)}></button>
                </div>
                <div className="modal-body">
                  <pre className="json-pre">{JSON.stringify(modalData, null, 2)}</pre>
                </div>
                <div className="modal-footer">
                  <button className="btn btn-secondary" onClick={() => setModalData(null)}>Close</button>
                </div>
              </div>
            </div>
            <div className="modal-backdrop show" />
          </div>
        )}
      </div>
    </div>
  );
};

export default Teams;
