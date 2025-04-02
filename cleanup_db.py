import sqlite3
import time

DB_PATH = "sensors.db"  # Path to the SQLite database

def cleanup_old_entries(max_age_days=7):
    """
    Deletes entries from the sensor_data_db table that are older than max_age_days.
    """
    # Calculate the cutoff time
    cutoff_time = time.time() - max_age_days * 86400  # Convert days to seconds
    cutoff_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cutoff_time))

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    with conn:
        # Delete old entries
        conn.execute("DELETE FROM sensor_data_db WHERE time < ?", (cutoff_date,))
        print(f"[INFO] Deleted entries older than {cutoff_date}")

if __name__ == "__main__":
    while True:
        cleanup_old_entries(max_age_days=7)
        time.sleep(3600)  # Run cleanup every hour
