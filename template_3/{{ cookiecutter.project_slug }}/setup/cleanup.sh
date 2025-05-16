#!/bin/bash

echo "Cleaning Pixi environment..."
pixi clean
echo "Pixi environment cleaned."

echo
echo "Do you want to clean data directories (raw and processed)? [y/N]"
read -r clean_data

if [[ $clean_data == "y" || $clean_data == "Y" ]]; then
    echo "Cleaning data directories..."
    # if [ -d "../data/raw" ]; then rm -rf ../data/raw/*; fi
    # if [ -d "../data/processed" ]; then rm -rf ../data/processed/*; fi
    echo "Data directories cleaned."
else
    echo "Data directories left intact."
fi

echo "Cleanup completed."
