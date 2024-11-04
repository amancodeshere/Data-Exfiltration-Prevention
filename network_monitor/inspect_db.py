import sqlite3

# This was mainly used to test the database.
# This is not used in the main functionality of the product.

def inspect_db():
    """
    Prints out all suspicious packets stored in the database to the console.
    """
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()

    c.execute('SELECT * FROM suspicious_packets ORDER BY timestamp DESC')
    packets = c.fetchall()

    conn.close()

    for packet in packets:
        print(packet)

if __name__ == "__main__":
    inspect_db()
