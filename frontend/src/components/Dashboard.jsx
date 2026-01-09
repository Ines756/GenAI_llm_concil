import { useState, useEffect } from 'react';
import './Dashboard.css';

export default function Dashboard() {
  const [data, setData] = useState({ health: {}, performance: {}, network: {} });

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/models/status');
        if (res.ok) {
          const json = await res.json();
          setData(json);
        }
      } catch (e) { console.error("Monitoring error", e); }
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  // --- LOGIQUE DES BADGES ---
  const onlineModels = Object.keys(data.performance).filter(
    m => data.health[m] === 'online' && data.performance[m].avg_latency > 0
  );

  // Modèle le plus rapide
  const fastestModel = onlineModels.length > 0 
    ? onlineModels.reduce((prev, curr) => 
        data.performance[prev].avg_latency < data.performance[curr].avg_latency ? prev : curr)
    : null;

  // Modèle le plus fiable (100% success rate)
  const reliableModels = onlineModels.filter(m => data.performance[m].success_rate === "100.0%");

  return (
    <div className="model-dashboard">
      {Object.keys(data.health).map(model => {
        const stats = data.performance[model] || { avg_latency: 0, total: 0, success_rate: "0%" };
        const ip = data.network[model] || "Inconnu";
        const isOnline = data.health[model] === 'online';

        return (
          <div key={model} className={`model-card ${isOnline ? 'online' : 'offline'}`}>
            <div className="card-header">
              <div className="status-dot"></div>
              <span className="model-name">{model}</span>
              {model === "mistral:latest" && <span className="badge chairman">Chairman</span>}
            </div>

            <div className="network-info">
              <span className="ip-label">Node IP:</span>
              <span className="ip-address">{ip}</span>
            </div>

            <div className="stats-row">
              <span className="latency">
                {stats.total > 0 ? `⚡ ${stats.avg_latency}s` : '⏳ No data'}
              </span>
              <div className="badges-container">
                {model === fastestModel && isOnline && <span className="badge fastest">🚀 Fastest</span>}
                {reliableModels.includes(model) && isOnline && stats.total > 0 && 
                  <span className="badge reliable">🛡️ Reliable</span>}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}