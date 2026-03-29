#!/usr/bin/env python3
"""Quick test to verify SMTP connectivity from Python."""
import socket
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing SMTP connection...")
print(f"SMTP Host: {os.getenv('SMTP_HOST', 'smtp.gmail.com')}")
print(f"SMTP Port: {os.getenv('SMTP_PORT', '587')}")

# Test 1: DNS resolution from Python
try:
    print("\n1. DNS Resolution Test...")
    addr_info = socket.getaddrinfo('smtp.gmail.com', 587, socket.AF_INET)
    print(f"   ✓ Resolved to: {addr_info[0][4][0]}")
except Exception as e:
    print(f"   ✗ DNS failed: {e}")
    exit(1)

# Test 2: Socket connection
try:
    print("\n2. Socket Connection Test...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    sock.connect(('smtp.gmail.com', 587))
    print("   ✓ Socket connection successful")
    sock.close()
except Exception as e:
    print(f"   ✗ Socket connection failed: {e}")
    exit(1)

# Test 3: SMTP connection
try:
    print("\n3. SMTP Connection Test...")
    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    server.ehlo()
    print("   ✓ SMTP connection successful")
    server.quit()
except Exception as e:
    print(f"   ✗ SMTP connection failed: {e}")
    exit(1)

print("\n✅ All tests passed! SMTP is reachable from Python.")
print("\nIf digest still fails, check .env credentials:")
print("  - SMTP_USER")
print("  - SMTP_PASSWORD (use App Password for Gmail)")
print("  - EMAIL_ENABLED=true")
