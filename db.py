import mysql.connector
import pandas as pd

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="DRroot@18#24",
        database="devops_metrics"
    )

def fetch_recent_metrics(minutes=10):
    conn = get_db_connection()

    query = f"""
    SELECT
        pod_name,
        cpu_usage,
        memory_usage / 1024 / 1024 AS memory_usage, -- bytes → MB
        restarts AS restart_count,
        timestamp
    FROM pod_metrics
    WHERE timestamp >= NOW() - INTERVAL {minutes} MINUTE
    ORDER BY timestamp
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df
