def calculate_health(cpu, memory, disk):
    """Return an overall health score out of 100"""
    health = 100 - (cpu * 0.3 + memory * 0.5 + disk * 0.2)
    return round(max(0, min(100, health)), 2)


def detect_anomaly(cpu_history):
    """Simple anomaly detection logic"""
    if len(cpu_history) < 3:
        return False
    avg = sum(cpu_history) / len(cpu_history)
    deviation = abs(cpu_history[-1] - avg)
    return deviation > 50  # basic threshold
