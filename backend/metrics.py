import time
from typing import Dict, List

# Stockage global simple
model_stats = {}

def update_metric(model_name: str, latency: float, success: bool):
    if model_name not in model_stats:
        model_stats[model_name] = {"latencies": [], "total_requests": 0, "success_count": 0}
    
    stats = model_stats[model_name]
    stats["total_requests"] += 1
    if success:
        stats["success_count"] += 1
        stats["latencies"].append(latency)
        # On ne garde que les 20 dernières mesures pour la moyenne
        if len(stats["latencies"]) > 20:
            stats["latencies"].pop(0)

def get_performance_data():
    report = {}
    for model, data in model_stats.items():
        lats = data["latencies"]
        report[model] = {
            "avg_latency": round(sum(lats) / len(lats), 2) if lats else 0,
            "total": data["total_requests"],
            "success_rate": f"{(data['success_count'] / data['total_requests']) * 100:.1f}%"
        }
    return report