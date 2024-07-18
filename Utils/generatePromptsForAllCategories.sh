#!/bin/bash

# Loop through categories from 1 to 21
for category in {1..21}; do
    # Run the script with the specified parameters
    python3 Utils/promptGenerator.py --category $category --strategy "15 at a time" --amount 500
done
