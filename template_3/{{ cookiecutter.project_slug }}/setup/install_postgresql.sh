#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


echo
echo -e "${YELLOW}PostgreSQL Installation${NC}"
echo

# Check if PostgreSQL is already installed
if command -v psql &> /dev/null; then
    echo "PostgreSQL is already installed"
    psql --version
else
    echo "Installing PostgreSQL..."
    
	# Update the package list
    sudo apt update

    # Install PostgreSQL and its contrib package
    sudo apt install -y postgresql postgresql-contrib
    
    echo "PostgreSQL installation completed."
fi

# Ensure PostgreSQL service is running
if systemctl is-active --quiet postgresql; then
    echo "PostgreSQL service is already running"
else
    echo "Starting PostgreSQL service..."
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    echo "PostgreSQL service started"
fi

echo -e "${GREEN}PostgreSQL installation and setup completed successfully!${NC}"
