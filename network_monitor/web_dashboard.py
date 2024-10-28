# web_dashboard.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import sqlite3
from geo_ip import get_geo_location, is_private_ip  # Import the geolocation function and private IP check
import signal
import sys

app = Flask(__name__)
socketio = SocketIO(app)

def get_packets():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM suspicious_packets ORDER BY timestamp DESC')
    packets = c.fetchall()
    conn.close()
    
    packets_with_location = []
    for packet in packets:
        src_ip = packet[1]
        if is_private_ip(src_ip):
            location = "Private IP Range"
        else:
            geo_info = get_geo_location(src_ip)
            city = geo_info.get('city', 'N/A')
            country = geo_info.get('country', 'N/A')
            location = f"{city}, {country}"
        packets_with_location.append((*packet, location))
    
    return packets_with_location

def get_blocked_transfers():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM blocked_transfers ORDER BY timestamp DESC')
    blocked_transfers = c.fetchall()
    conn.close()
    return blocked_transfers

@app.route('/')
def index():
    packets = get_packets()
    blocked_transfers = get_blocked_transfers()
    return render_template('index.html', packets=packets, blocked_transfers=blocked_transfers)

def notify_new_packet(packet):
    socketio.emit('new_packet', packet)

def signal_handler(signal, frame):
    # Clear the database
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('DELETE FROM blocked_transfers')
    conn.commit()
    conn.close()
    print("Database cleared.")
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    app.run(debug=True, use_reloader=False)
