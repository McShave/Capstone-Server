# By Minhwan. Just for testing

from flask import Flask, render_template, jsonify
import sys
import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
# Add the parent directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from db_handler import DBHandler
import multiprocessing
import subprocess

app = Flask(__name__)
db = DBHandler()

# Route: Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Route: Get Sensor Data
@app.route("/api/sensor_data")
def get_sensor_data():
    with db.create_connection() as conn:
        cursor = conn.execute("SELECT sensors_db.name, sensor_data_db.time, sensor_data_db.value FROM sensor_data_db JOIN sensors_db ON sensors_db.id = sensor_data_db.f_id ORDER BY sensor_data_db.time DESC LIMIT 50")
        data = [{"sensor": row[0], "time": row[1], "value": row[2]} for row in cursor.fetchall()]
    return jsonify(data)

# Route: View Logs
@app.route("/logs")
def logs():
    return render_template("logs.html")

# Function to run BLE client
def run_ble_client():
    subprocess.run(["python3", "/home/pi/capstone_project/BLEclient.py"])

# Function to run cleanup script periodically
def run_cleanup():
    subprocess.run(["python3", "/home/pi/capstone_project/cleanup_db.py"])

if __name__ == "__main__":
    # Start BLE client in parallel with Flask app
    ble_process = multiprocessing.Process(target=run_ble_client)
    ble_process.start()

    # Start cleanup scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_cleanup, 'interval', days=1)  # Run cleanup every 24 hours
    scheduler.start()

    try:
        # Start Flask app
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        # Ensure BLE client is terminated when Flask app stops
        ble_process.terminate()
        scheduler.shutdown()
