from flask import Flask, render_template
import sqlite3
import time

app = Flask(__name__)

DB_FILE = "exfiltration_alerts.db"

def fetch_alerts():
    """Fetch alerts from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Alerts ORDER BY id DESC")  # Fetch alerts in descending order
    alerts = cursor.fetchall()
    conn.close()
    return alerts

@app.route('/')
def index():
    """Render the index page with alerts."""
    alerts = fetch_alerts()
    return render_template('index.html', alerts=alerts)

@app.route('/refresh')
def refresh():
    """Fetch and return latest alerts as a JSON response."""
    alerts = fetch_alerts()
    return {'alerts': alerts}

if __name__ == "__main__":
    app.run(debug=True)
