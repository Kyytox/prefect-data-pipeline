#!/bin/bash

# Main setup script for data engineering project

# Create directories if they don't exist
# mkdir -p ../data/raw
# mkdir -p ../data/processed

# Set script directory to be executable
chmod +x ./setup/*.sh

echo "======================================="
echo "Prefect Data Pipeline Project Setup"
echo "======================================="
echo

PS3="Select an option (1-6): "
# options=("Run All Setup" "Install PostgreSQL" "Install Dependencies" "Setup Database" "Cleanup" "Exit")

select opt in "Run All Setup" "Install PostgreSQL" "Install Dependencies" "Setup Database" "Cleanup" "Exit"
do
    case $opt in
        "Run All Setup")
            echo
            echo "Running complete setup..."
            ./setup/install_postgresql.sh
            ./setup/init_database.sh
            ./setup/install_dependencies.sh
            echo "All setup completed successfully!"
            echo
            ;;
        "Install PostgreSQL")
            echo
            echo "Installing PostgreSQL..."
            ./setup/install_postgresql.sh
            echo
            ;;
        "Install Dependencies")
            echo
            echo "Installing dependencies..."
            ./setup/install_dependencies.sh
            echo
            ;;
        "Setup Database")
            echo
            echo "Setting up database..."
            ./setup/init_database.sh
            echo
            ;;
        "Cleanup")
            echo
            echo "Running cleanup..."
            ./setup/cleanup.sh
            echo
            ;;
        "Exit")
            echo "Exiting setup."
            break
            ;;
        *)
            echo "Invalid option $REPLY"
            ;;
    esac
    echo "======================================="
    echo
done