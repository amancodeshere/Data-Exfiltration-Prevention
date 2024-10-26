# web_dashboard.py
from flask import Flask, render_template
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)

def get_packets():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM suspicious_packets ORDER BY timestamp DESC')
    packets = c.fetchall()
    conn.close()
    return packets

@app.route('/')
def index():
    packets = get_packets()
    return render_template('index.html', packets=packets)

def notify_new_packet(packet):
    socketio.emit('new_packet', packet)

if __name__ == '__main__':
    socketio.run(app, debug=True)
