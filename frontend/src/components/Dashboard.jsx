import { useState, useEffect } from 'react';
import './Dashboard.css';

export default function Dashboard() {
  const [data, setData] = useState({ health: {}, performance: {} });

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch('http://localhost:8000/api/models/status');
        if (res.ok) {
          const json = await res.json();
          setData(json);
        }
      } catch (e) {
        console.error("Erreur Monitoring:", e);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="model-dashboard">
      {Object.keys(data.health).map(model => {
        // Sécurité : on vérifie si les perfs existent pour ce modèle
        const stats = data.performance[model] || { avg_latency: 0, total: 0 };
        const isOnline = data.health[model] === 'online';

        return (
          <div key={model} className={`model-card ${isOnline ? 'online' : 'offline'}`}>
            <div className="status-dot"></div>
            <div className="model-info">
              <span className="model-name">{model}</span>
              <div className="model-stats">
                <span className="latency">
                  {stats.total > 0 ? `${stats.avg_latency}s` : 'En attente...'}
                </span>
                {/* On identifie le Chairman via le nom du modèle défini dans config.py */}
                {model === "mistral:latest" && <span className="badge-chairman">Chairman</span>}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}