# web_dashboard.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import sqlite3
from geo_ip import get_geo_location, is_private_ip

app = Flask(__name__)
socketio = SocketIO(app)

def get_packets():
    """
    Fetches suspicious packets from the database, ordered by timestamp
    It also adds the geolocation of each packet (source IP)

    Returns:
         A list of tuples, each containing the packet's ID, source IP
             address, destination IP address, timestamp, and location.
    """
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM suspicious_packets ORDER BY timestamp DESC')
    packets = c.fetchall()
    conn.close()
    
    # Add geolocation data to packets
    packetsWithLocation = []
    for packet in packets:
        sourceIP = packet[1]
        if is_private_ip(sourceIP):
            location = "Private IP Range"
        else:
            geo_info = get_geo_location(sourceIP)
            city = geo_info.get('city', 'N/A')
            country = geo_info.get('country', 'N/A')
            location = f"{city}, {country}"
        packetsWithLocation.append((*packet, location))
    
    # Debug print statement
    print("Fetched packets:", packetsWithLocation)
    return packetsWithLocation

@app.route('/')
def index():
    """
    Handle the root URL '/' and render the index page

    Returns:
        The rendered HTML of the index page with the packets data.
    """
    packets = get_packets()
    return render_template('index.html', packets=packets)

def notify_new_packet(packet):
    """
    Notify the client of a new packet.

    Args:
        packet (tuple): A tuple containing the packet's ID, source IP address,
            destination IP address, timestamp, and location.
    """
    socketio.emit('new_packet', packet)
    socketio.emit('new_packet', packet)

if __name__ == '__main__':
    socketio.run(app, debug=True)
