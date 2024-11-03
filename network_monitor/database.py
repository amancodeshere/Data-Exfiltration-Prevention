# database.py
import sqlite3

def init_db():
    """
    Initializes the  database and sets up the
    suspicious_packets table.
    """
    # Connect to database
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()

    # Drop table if it exists
    c.execute("DROP TABLE IF EXISTS suspicious_packets;")

    # Create a new table
    c.execute('''
        CREATE TABLE IF NOT EXISTS suspicious_packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            src_ip TEXT,
            dest_ip TEXT,
            timestamp DATETIME
        )
    ''')

    # Commit changes and close
    conn.commit()
    conn.close()


def log_packet(src_ip, dest_ip, timestamp):
    """
    Logs a network packet's source and destination IP addresses to the database.

    Arguments:
        src_ip (str): The source IP address of the packet.
        dest_ip (str): The destination IP address of the packet.
        timestamp: The time of the packet.
    Returns:
        None
    """
    # Connect to database
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    # Insert into database
    c.execute('''
        INSERT INTO suspicious_packets (src_ip, dest_ip, timestamp) VALUES (?, ?, ?)
    ''', (src_ip, dest_ip, timestamp))

    # Commit changes and close
    conn.commit()
    conn.close()
