#!/bin/bash


# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


echo
echo -e "${YELLOW}Setting up database...${NC}"
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

echo "Creating/Updating tables..."
sudo -u postgres psql -f ./setup/create_table.sql
echo "Tables setup completed."

echo -e "${GREEN}Database setup completed successfully!${NC}"