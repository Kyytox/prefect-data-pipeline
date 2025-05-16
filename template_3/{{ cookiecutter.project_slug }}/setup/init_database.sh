#!/bin/bash

echo "Setting up database..."
echo 

# Check if database already exists
DB_EXISTS=$(sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='{{ cookiecutter.database_name }}'")

if [ "$DB_EXISTS" = "1" ]; then
    echo "Database {{ cookiecutter.database_name }} already exists."
else
    echo "Initializing database..."
    sudo -u postgres psql -f ./setup/create_db.sql
    echo "Database initialized."
fi

echo 
echo "Creating/Updating tables..."
echo
sudo -u postgres psql -f ./setup/create_table.sql
echo "Tables setup completed."

echo "Database setup completed successfully."
