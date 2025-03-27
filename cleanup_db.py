import sqlite3
import time

DB_PATH = "sensors.db"

def cleanup_old_entries(max_age_days=7):
    cutoff_time = time.time() - max_age_days * 86400
    cutoff_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cutoff_time))

    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute("DELETE FROM sensor_data_db WHERE time < ?", (cutoff_date,))
        print(f"[INFO] Deleted entries older than {cutoff_date}")

if __name__ == "__main__":
    cleanup_old_entries()
