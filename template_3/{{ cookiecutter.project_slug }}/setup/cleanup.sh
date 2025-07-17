#!/bin/bash


# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Delete database
echo
echo -e "${YELLOW}Starting cleanup...${NC}"
echo


# Delete database if it exists
echo "Deleting database..."
sudo -u postgres psql -f ./setup/delete_db.sql
echo -e "${GREEN}Database deleted successfully!${NC}"

# Clean pixi environment
echo "Cleaning Pixi environment..."
pixi clean
echo -e "${GREEN}Pixi environment cleaned successfully!${NC}"


echo
echo
echo -e "${GREEN}Cleanup completed successfully!${NC}"
echo -e "run ${RED}'exit'${NC} to exit the pixi shell"
echo
echo