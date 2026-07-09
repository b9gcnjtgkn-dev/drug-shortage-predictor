"use client";

import { useState, useEffect } from 'react';

export default function Home() {
  const [reason, setReason] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [historicalData, setHistoricalData] = useState([]);

  // Fetch historical data on mount
  useEffect(() => {
    fetch("http://localhost:8000/api/historical")
      .then(res => res.json())
      .then(data => {
        if (data.data) {
          setHistoricalData(data.data.slice(0, 10)); // Just show top 10 for dashboard
        }
      })
      .catch(err => console.error("Failed to fetch historical data", err));
  }, []);

  const handlePredict = async () => {
    if (!reason.trim()) return;
    
    setLoading(true);
    setPrediction(null);
    
    try {
      const response = await fetch("http://localhost:8000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ termination_reason: reason })
      });
      
      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      console.error("Prediction failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <header>
        <h1>Drug Shortage Predictor AI</h1>
        <p>Predicting FDA injectable drug shortages 3-18 months in advance from ClinicalTrials.gov termination signals.</p>
      </header>

      <div className="dashboard-grid">
        <section className="glass-card">
          <div className="input-group">
            <label htmlFor="reason">Clinical Trial Termination Reason</label>
            <textarea 
              id="reason"
              placeholder="e.g. Trial was terminated due to manufacturing delays and supply chain issues..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            ></textarea>
            <button 
              className="btn" 
              onClick={handlePredict}
              disabled={loading || !reason.trim()}
            >
              {loading ? "Analyzing Signal..." : "Predict Shortage Risk"}
            </button>
          </div>
        </section>

        <section className="glass-card result-section">
          <h2>Prediction Result</h2>
          {prediction ? (
            <>
              <div className={`risk-circle ${prediction.high_risk ? 'high-risk' : 'low-risk'}`}>
                <span className="risk-percentage">{Math.round(prediction.shortage_risk_probability * 100)}%</span>
                <span className="risk-label">Risk</span>
              </div>
              <p>
                {prediction.high_risk 
                  ? "High probability of shortage within 3-18 months based on historical termination patterns." 
                  : "Low probability of shortage."}
              </p>
            </>
          ) : (
            <p style={{marginTop: '2rem', color: 'var(--text-secondary)'}}>
              Enter a termination reason to see the AI prediction.
            </p>
          )}
        </section>
      </div>

      <section className="data-table-container glass-card">
        <h2>Recent Terminated Trials (Training Dataset)</h2>
        <table>
          <thead>
            <tr>
              <th>NCT ID</th>
              <th>Drug Name</th>
              <th>Termination Date</th>
              <th>Shortage Occurred (3-18mo)</th>
            </tr>
          </thead>
          <tbody>
            {historicalData.map((row, i) => (
              <tr key={i}>
                <td>{row.nct_id}</td>
                <td>{row.drug_name}</td>
                <td>{row.termination_date}</td>
                <td>{row.shortage_occurred === 1 ? '✅ Yes' : '❌ No'}</td>
              </tr>
            ))}
            {historicalData.length === 0 && (
              <tr>
                <td colSpan="4" style={{textAlign: 'center'}}>No historical data available. Ensure backend is running.</td>
              </tr>
            )}
          </tbody>
        </table>
      </section>
    </main>
  );
}
