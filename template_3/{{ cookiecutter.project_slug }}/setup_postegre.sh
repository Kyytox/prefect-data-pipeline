#!/bin/bash

# Update the package list
sudo apt update

# Install PostgreSQL and its contrib package
sudo apt install -y postgresql postgresql-contrib

echo "PostgreSQL installation completed."