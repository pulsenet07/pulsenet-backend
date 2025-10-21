from app.db import conn, cursor
import psycopg2

def ensure_database_integrity():
    try:
        cursor.execute("SELECT 1 FROM agents LIMIT 1;")
        cursor.execute("SELECT 1 FROM pulses LIMIT 1;")
        conn.commit()
        print("✅ Database integrity check passed.")
    except psycopg2.errors.UndefinedTable:
        print("⚠️ Tables missing in database.")
        choice = input("Do you want to recreate the tables? (y/n): ")
        if choice.lower() == 'y':
            recreate_tables()
        else:
            print("Exiting...")
            exit(1)
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        choice = input("Recreate the database from scratch? (y/n): ")
        if choice.lower() == 'y':
            recreate_tables()
        else:
            print("Exiting...")
            exit(1)

def recreate_tables():
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id SERIAL PRIMARY KEY,
                agent_id VARCHAR(100),
                api_key TEXT,
                fingerprint TEXT,
                registered_at TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pulses (
                id SERIAL PRIMARY KEY,
                agent_id VARCHAR(100),
                timestamp TIMESTAMP,
                cpu_usage FLOAT,
                memory_usage FLOAT,
                disk_usage FLOAT
            );
        """)
        conn.commit()
        print("✅ Database recreated successfully.")
    except Exception as e:
        print(f"❌ Failed to recreate database: {e}")
        exit(1)
