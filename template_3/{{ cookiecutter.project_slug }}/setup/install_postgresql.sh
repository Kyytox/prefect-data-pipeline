#!/bin/bash

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

echo "PostgreSQL setup completed successfully."
