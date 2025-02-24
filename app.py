from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Raspberry Pi!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # SQLite File Location
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turning off unnecessary settings 
db = SQLAlchemy(app)


### DataBase(SQLite3) code: 
import sqlite3

# Connect to database file
conn = sqlite3.connect('sensor_data.db')

# Create cursor
cursor = conn.cursor()

# Create Table, implementing SQL
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SensorData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_id TEXT NOT NULL,
        sensor_type TEXT NOT NULL,
        sensor_value REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
''')

# Commit and close the connection
conn.commit()
conn.close()
