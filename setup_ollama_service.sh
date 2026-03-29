#!/bin/bash
# Script to setup Ollama as a systemd service

echo "Creating Ollama systemd service..."

# Create systemd service file
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=$USER
ExecStart=$(which ollama) serve
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable ollama.service
sudo systemctl start ollama.service

# Check status
sudo systemctl status ollama.service

echo ""
echo "✅ Ollama service installed!"
echo ""
echo "Commands:"
echo "  sudo systemctl start ollama    # Start"
echo "  sudo systemctl stop ollama     # Stop"
echo "  sudo systemctl restart ollama  # Restart"
echo "  sudo systemctl status ollama   # Check status"
