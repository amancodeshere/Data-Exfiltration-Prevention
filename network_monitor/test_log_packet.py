# test_log_packet.py
from database import log_packet
from inspect_db import inspect_db

# Manually log a test packet
log_packet("192.168.1.1", "8.8.8.8")

# Check if packet is stored correctly
inspect_db()
