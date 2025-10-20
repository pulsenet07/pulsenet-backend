import psycopg2
import os

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "pulsenet"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASS", "Thinkinarealway@2005")
)
cursor = conn.cursor()
