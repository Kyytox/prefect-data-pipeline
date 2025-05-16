#!/bin/bash

# Main run script for data engineering project

echo "======================================="
echo "Data Engineering Project Runner"
echo "======================================="
echo

PS3="Select an option (1-3): "
options=("Run Main Pipeline" "Run with Custom Parameters" "Exit")

select opt in "${options[@]}"
do
    case $opt in
        "Run Main Pipeline")
            echo "Running main pipeline..."
            cd ..
            pixi run python main.py
            echo
            ;;
        "Run with Custom Parameters")
            echo "Enter custom parameters:"
            read -r params
            echo "Running with custom parameters: $params"
            cd ..
            pixi run python main.py $params
            echo
            ;;
        "Exit")
            echo "Exiting runner."
            break
            ;;
        *) 
            echo "Invalid option $REPLY"
            ;;
    esac
    echo "======================================="
    echo
done
