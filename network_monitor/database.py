# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS suspicious_packets;")
    c.execute('''
        CREATE TABLE IF NOT EXISTS suspicious_packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src_ip TEXT,
            dest_ip TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_packet(src_ip, dest_ip):
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO suspicious_packets (src_ip, dest_ip) VALUES (?, ?)
    ''', (src_ip, dest_ip))
    conn.commit()
    conn.close()
