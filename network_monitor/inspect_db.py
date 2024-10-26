import sqlite3

def inspect_db():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    c.execute('SELECT * FROM suspicious_packets ORDER BY timestamp DESC')
    packets = c.fetchall()
    conn.close()
    for packet in packets:
        print(packet)

if __name__ == "__main__":
    inspect_db()
