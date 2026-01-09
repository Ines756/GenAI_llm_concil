import time
from typing import Dict, List

import json
import os

METRICS_FILE = "data/metrics.json"

def load_metrics():
    if os.path.exists(METRICS_FILE):
        try:
            with open(METRICS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_metrics(stats):
    os.makedirs("data", exist_ok=True)
    with open(METRICS_FILE, "w") as f:
        json.dump(stats, f)

# Initialisation au démarrage
model_stats = load_metrics()

def update_metric(model_name: str, latency: float, success: bool):
    global model_stats
    if model_name not in model_stats:
        model_stats[model_name] = {"latencies": [], "total_requests": 0, "success_count": 0}
    
    stats = model_stats[model_name]
    stats["total_requests"] += 1
    if success:
        stats["success_count"] += 1
        stats["latencies"].append(latency)
        if len(stats["latencies"]) > 20:
            stats["latencies"].pop(0)
    
    # On sauvegarde après chaque mise à jour
    save_metrics(model_stats)

def get_performance_data():
    report = {}
    for model, data in model_stats.items():
        lats = data.get("latencies", [])
        total = data.get("total_requests", 0)
        success_count = data.get("success_count", 0)
        
        report[model] = {
            "avg_latency": round(sum(lats) / len(lats), 2) if lats else 0,
            "total": total,
            "success_rate": f"{(success_count / total) * 100:.1f}%" if total > 0 else "0.0%"
        }
    return report