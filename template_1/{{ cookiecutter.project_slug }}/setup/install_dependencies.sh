#!/bin/bash


# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


echo
echo -e "${YELLOW}Installing dependencies with Pixi...${NC}"
echo

# Check if pixi is installed
if ! command -v pixi &> /dev/null; then
    echo "Error: Pixi is not installed. Please install pixi first."
    echo "Visit https://pixi.sh for installation instructions."
    exit 1
fi

# Install dependencies using pixicd ..
pixi install

# Activate the pixi environment
echo
echo -e "${GREEN}Dependencies installed successfully and pixi shell started!${NC}"
echo "Starting pixi shell (use 'exit' to return to normal shell)..."
pixi shell



