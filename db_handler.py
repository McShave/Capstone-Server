import sqlite3

class DBHandler:
    def __init__(self, db_path="sensors.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS sensors_db (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data_db (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    f_id INTEGER,
                    time TEXT,
                    value TEXT,
                    FOREIGN KEY (f_id) REFERENCES sensors_db (id)
                )
            """)

    def reset_auto_increment(self):
        """Reset the auto-increment counter for sensors_db if the table is empty."""
        with self.conn:
            cursor = self.conn.execute("SELECT COUNT(*) FROM sensors_db")
            count = cursor.fetchone()[0]
            if count == 0:  # If the table is empty
                self.conn.execute("DELETE FROM sqlite_sequence WHERE name='sensors_db'")
                print("[INFO] Reset auto-increment for sensors_db.")

    def add_sensor(self, name):
        if not name or name.strip() == "":  # Skip empty or invalid names
            return None
        with self.conn:
            self.reset_auto_increment()  # Ensure auto-increment is reset if the table is empty
            cursor = self.conn.execute("INSERT OR IGNORE INTO sensors_db (name) VALUES (?)", (name,))
            if cursor.lastrowid:  # If a new row was inserted
                return cursor.lastrowid
            # If the sensor already exists, fetch its ID
            cursor = self.conn.execute("SELECT id FROM sensors_db WHERE name = ?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_sensor_id_by_uuid(self, uuid):
        cursor = self.conn.execute("SELECT id FROM sensors_db WHERE name = ?", (uuid,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_sensor_name_by_uuid(self, uuid):
        cursor = self.conn.execute("SELECT name FROM sensors_db WHERE name = ?", (uuid,))
        result = cursor.fetchone()
        return result[0] if result else None

    def add_sensor_data(self, f_id, time, value):
        with self.conn:
            self.conn.execute("INSERT INTO sensor_data_db (f_id, time, value) VALUES (?, ?, ?)", (f_id, time, value))
            print(f"[INFO] Added sensor data: f_id={f_id}, time={time}, value={value}")

    def remove_sensor_data_by_device(self, device_address):
        with self.conn:
            self.conn.execute("DELETE FROM sensor_data_db WHERE f_id IN (SELECT id FROM sensors_db WHERE name = ?)", (device_address,))
