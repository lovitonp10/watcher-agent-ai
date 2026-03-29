#!/bin/bash

# Tech Watch Agent - Daily Digest Scheduler
# Run this script to send the daily digest email

# Set working directory (change this to your actual path)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Run digest command
python main.py digest

# Log execution
echo "Digest executed at $(date)" >> digest.log
