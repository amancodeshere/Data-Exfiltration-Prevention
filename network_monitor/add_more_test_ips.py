import sqlite3

def add_more_test_ips():
    conn = sqlite3.connect('network_monitor.db')
    c = conn.cursor()
    more_test_ips = [
        ('23.67.253.113', '8.8.8.8'),  # Akamai Technologies
        ('13.35.14.14', '8.8.4.4'),  # Amazon AWS
        ('40.112.72.205', '1.1.1.1'),  # Microsoft Azure
        ('31.13.69.229', '208.67.222.222'),  # Facebook
        ('104.244.42.129', '9.9.9.9')  # Twitter
    ]
    for src_ip, dest_ip in more_test_ips:
        c.execute('''INSERT INTO suspicious_packets (src_ip, dest_ip) VALUES (?, ?)''', (src_ip, dest_ip))
    conn.commit()
    conn.close()
    print("More test IPs added to the database.")

if __name__ == "__main__":
    add_more_test_ips()
