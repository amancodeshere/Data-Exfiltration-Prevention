# tests/test_database.py
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3 
import unittest
import os
from database import init_db, log_packet

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Remove the database file if it exists and initialize the database
        if os.path.exists('network_monitor.db'):
            os.remove('network_monitor.db')
        init_db()

    def test_log_packet(self):
        # Log a packet and check if it's stored correctly
        src_ip = '192.168.1.1'
        dest_ip = '8.8.8.8'
        log_packet(src_ip, dest_ip)

        # Query the database to check if the packet was logged
        conn = sqlite3.connect('network_monitor.db')
        c = conn.cursor()
        c.execute('SELECT * FROM suspicious_packets WHERE src_ip=? AND dest_ip=?', (src_ip, dest_ip))
        result = c.fetchone()
        conn.close()

        self.assertIsNotNone(result, "Packet should be logged in the database.")
        self.assertEqual(result[1], src_ip, "Source IP should match the logged packet.")
        self.assertEqual(result[2], dest_ip, "Destination IP should match the logged packet.")

    def test_database_initialization(self):
        # Check if the database file is created
        conn = sqlite3.connect('network_monitor.db')
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='suspicious_packets'")
        result = c.fetchone()
        conn.close()

        self.assertIsNotNone(result, "Database should contain the 'suspicious_packets' table.")

if __name__ == '__main__':
    unittest.main()
