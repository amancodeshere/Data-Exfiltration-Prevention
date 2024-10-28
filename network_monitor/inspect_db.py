import sqlite3

def inspect_db():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    print("Suspicious Packets:")
    c.execute('SELECT * FROM suspicious_packets ORDER BY timestamp DESC')
    packets = c.fetchall()
    for packet in packets:
        print(packet)
    
    print("\nBlocked Transfers:")
    c.execute('SELECT * FROM blocked_transfers ORDER BY timestamp DESC')
    blocked_transfers = c.fetchall()
    for transfer in blocked_transfers:
        print(transfer)
    
    conn.close()

if __name__ == "__main__":
    inspect_db()
