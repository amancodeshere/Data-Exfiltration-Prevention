# database.py
import sqlite3

def init_db():
    """
    Initializes the 'network_monitor.db' database and creates the
    'suspicious_packets' table if it does not already exist.

    This function is used to set up the database before logging any packets.
    It should be called once when the program is first run. The function
    deletes any existing 'suspicious_packets' table and then creates a new
    table with the same name and columns.

    The table has the following columns:
        id (INTEGER PRIMARY KEY AUTOINCREMENT): A unique identifier for
            each packet.
        src_ip (TEXT): The source IP address of the packet.
        dest_ip (TEXT): The destination IP address of the packet.
        timestamp (DATETIME DEFAULT CURRENT_TIMESTAMP): The time the packet
            was logged.

    The function commits the changes to the database and then closes the
    connection.
    """
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
    """
    Logs a network packet's source and destination IP addresses to the database.

    Args:
        src_ip (str): The source IP address of the packet.
        dest_ip (str): The destination IP address of the packet.

    The function inserts an entry into the 'suspicious_packets' table in the
    'network_monitor.db' database, which includes the source IP, destination IP,
    and the current timestamp.
    """
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO suspicious_packets (src_ip, dest_ip) VALUES (?, ?)
    ''', (src_ip, dest_ip))
    conn.commit()
    conn.close()
