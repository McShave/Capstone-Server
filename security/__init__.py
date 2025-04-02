import os
import sys
import asyncio  # Import asyncio
import multiprocessing
import subprocess
from flask import Flask, render_template, jsonify
from .auth import auth  # Keep authentication
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Process

# Add the parent directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from cleanup_db import cleanup_old_entries  # Changed to absolute import
from BME_BLEclient import main as bme_main
from Water_BLEclient import main as water_main
from Smoke_BLEclient import main as smoke_main
from db_handler import DBHandler  # Import the custom database handler

sensor_db = DBHandler()

def start_background_tasks():
    """
    Start BLE clients and cleanup script as background processes.
    """
    # Wrapper to run asyncio coroutines in a new process
    def run_asyncio_coroutine(coroutine):
        asyncio.run(coroutine)

    # Start BLE clients
    bme_process = Process(target=run_asyncio_coroutine, args=(bme_main(),))
    water_process = Process(target=run_asyncio_coroutine, args=(water_main(),))
    smoke_process = Process(target=run_asyncio_coroutine, args=(smoke_main(),))

    # Start cleanup script
    cleanup_process = Process(target=cleanup_old_entries, kwargs={"max_age_days": 7})

    # Start all processes
    bme_process.start()
    water_process.start()
    smoke_process.start()
    cleanup_process.start()

    # Store processes for later management
    return [bme_process, water_process, smoke_process, cleanup_process]

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'security.sqlite'),
    )

    @app.route('/')
    def home():
        # Fetch sensor data from the database
        sensor_data = sensor_db.get_all_sensor_data()
        return render_template('home.html', sensor_data=sensor_data)

    @app.route('/api/sensor-data')
    def api_sensor_data():
        """
        API endpoint to fetch sensor data as JSON.
        """
        sensor_data = sensor_db.get_all_sensor_data()
        # Filter out invalid sensor names
        valid_sensor_data = [sensor for sensor in sensor_data if sensor["name"] not in ["\x00\x00", "Unknown Sensor"]]
        print(f"[DEBUG] Fetched valid sensor data: {valid_sensor_data}")  # Debug log
        return jsonify(valid_sensor_data)

    app.register_blueprint(auth)  # Keep login/register functionality

    from . import db
    db.init_app(app)

    # Start background tasks when the app starts
    processes = start_background_tasks()

    @app.teardown_appcontext
    def cleanup_processes(exception=None):
        for process in processes:
            process.terminate()

    return app

