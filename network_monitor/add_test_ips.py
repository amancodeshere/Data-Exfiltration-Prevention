# web_dashboard.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import sqlite3
from geo_ip import get_geo_location, is_private_ip  # Import the geolocation function and private IP check
import logging

app = Flask(__name__)
socketio = SocketIO(app)
logging.basicConfig(level=logging.DEBUG)

def get_packets():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM suspicious_packets ORDER BY timestamp DESC')
    packets = c.fetchall()
    conn.close()
    
    packets_with_location = []
    for packet in packets:
        src_ip = packet[1]
        try:
            if is_private_ip(src_ip):
                location = "Private IP Range"
            else:
                geo_info = get_geo_location(src_ip)
                city = geo_info.get('city', 'N/A')
                country = geo_info.get('country', 'N/A')
                location = f"{city}, {country}"
            packets_with_location.append((*packet, location))
        except Exception as e:
            logging.error(f"Error processing packet {packet}: {e}")
    
    return packets_with_location

@app.route('/')
def index():
    logging.debug("Serving index route")
    packets = get_packets()
    return render_template('index.html', packets=packets)

def notify_new_packet(packet):
    socketio.emit('new_packet', packet)

if __name__ == '__main__':
    logging.debug("Starting web dashboard")
    socketio.run(app, debug=True)
