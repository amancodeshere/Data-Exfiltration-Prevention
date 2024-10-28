import sqlite3

def add_test_blocked_transfers():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    test_transfers = [
        ('8.8.8.8', 'Blacklisted IP'),
        ('1.1.1.1', 'Prohibited location')
    ]
    for dest_ip, reason in test_transfers:
        c.execute('''
            INSERT INTO blocked_transfers (dest_ip, reason) VALUES (?, ?)
        ''', (dest_ip, reason))
    conn.commit()
    conn.close()
    print("Test blocked transfers added to the database.")

if __name__ == "__main__":
    add_test_blocked_transfers()
