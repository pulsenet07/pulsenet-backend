def create_pulse_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pulses (
            id SERIAL PRIMARY KEY,
            agent_id VARCHAR(100),
            timestamp TIMESTAMP,
            cpu NUMERIC,
            memory NUMERIC,
            disk NUMERIC,
            network_in NUMERIC,
            network_out NUMERIC,
            uptime VARCHAR(100),
            status VARCHAR(50),
            health_score NUMERIC
        )
    """)

def create_alerts_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            agent_id VARCHAR(100),
            timestamp TIMESTAMP,
            alert_type VARCHAR(50),
            description TEXT,
            severity VARCHAR(20)
        )
    """)

def init_tables(cursor):
    create_pulse_table(cursor)
    create_alerts_table(cursor)