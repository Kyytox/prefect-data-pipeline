#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

chmod +x ./setup/*.sh

show_menu() {
    echo
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${YELLOW}              Project Setup${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    echo -e "${GREEN}[1]${NC} Run All Setup"
    echo -e "${GREEN}[2]${NC} Install Dependencies"
    echo -e "${GREEN}[3]${NC} Cleanup"
    echo -e "${RED}[4]${NC} Exit"
    echo
    echo -n "Select an option: "
}

while true; do
    show_menu
    read -r choice
    
    case $choice in
        1)
            echo -e "\n${YELLOW}Running complete setup...${NC}"
            ./setup/install_dependencies.sh
            break
            ;;
        2)
            ./setup/install_dependencies.sh
            break
            ;;
        3)
            ./setup/cleanup.sh
            break
            ;;
        4)
            echo -e "${YELLOW}Exiting setup.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            sleep 2
            ;;
    esac
done