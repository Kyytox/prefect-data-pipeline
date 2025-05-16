#!/bin/bash

# echo "Setting up environment variables..."
# if [ -f ./.env ]; then
#     echo $DB_USER
#     set -a
#     source ./.env
#     set +a
#     echo $DB_USER
#     echo "Environment variables set."
# else
#     echo "Warning: .env file not found. Using default environment."
# fi

# echo
echo "Installing dependencies with Pixi..."

# Check if pixi is installed
if ! command -v pixi &> /dev/null; then
    echo "Error: Pixi is not installed. Please install pixi first."
    echo "Visit https://pixi.sh for installation instructions."
    exit 1
fi

# Install dependencies using pixicd ..
pixi install
echo "Dependencies installed successfully."
echo

echo "Starting pixi shell (use 'exit' to return to normal shell)..."
pixi shell
