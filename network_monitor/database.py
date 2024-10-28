# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS suspicious_packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src_ip TEXT,
            dest_ip TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS blocked_transfers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dest_ip TEXT,
            reason TEXT,
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

def log_blocked_transfer(dest_ip, reason):
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO blocked_transfers (dest_ip, reason) VALUES (?, ?)
    ''', (dest_ip, reason))
    conn.commit()
    conn.close()
