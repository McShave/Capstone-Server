import asyncio
import sqlite3
from bleak import BleakClient

# Define the ESP32 BLE address and characteristic UUID
ADDRESS = "3C:8A:1F:50:79:22"  # Update with your ESP32 BLE address
CHARACTERISTIC_UUID = "9f8230a6-3921-427a-99de-d675cf1352aa"  # Smoke sensor characteristic

# Define the database path (shared with the web server)
DATABASE_PATH = "/home/pi/capstone_project/security/sensor_data.db"

# Function to insert data into SQLite
def insert_data(smoke_level):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO smoke_data (smoke_level) VALUES (?, datetime('now'))", (smoke_level,))
        conn.commit()
        conn.close()
        print("Data inserted into database.")
    except Exception as e:
        print(f"Database Error: {e}")

async def read_smoke_sensor(address):
    try:
        async with BleakClient(address) as client:
            print(f"Connected to {address}")
            
            while True:
                # Read data from BLE characteristic
                smoke_level = await client.read_gatt_char(CHARACTERISTIC_UUID)
                smoke_level_str = smoke_level.decode("utf-8").strip()
                smoke_level = int(smoke_level_str)

                print(f"Smoke Level: {smoke_level}")

                # Insert data into the database
                insert_data(smoke_level)

                await asyncio.sleep(2)  # Wait for 2 seconds before reading again
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(read_smoke_sensor(ADDRESS))
    except KeyboardInterrupt:
        print("Disconnected from BLE device.")



