#!/bin/bash

# Specify the folder path
folder="/home/meulindux/AutostockUtils/Prompts"
source /home/meulindux/AutostockUtils/venv/bin/activate
export DISPLAY=:0
exec > >(tee -a log) 2>&1

# Get the current hour
current_hour=$(date +%H)

# Check if the current time is after 8 AM
if [ "$current_hour" -ge 8 ]; then
    # Initialize the files array
    files=()

    # Loop through each file in the folder, sorted numerically
    while IFS= read -r -d '' file; do
        # Check if the file is a regular file (not a directory)
        if [ -f "$file" ]; then
            files+=("$file") # Add the file to the array
        fi
    done < <(find "$folder" -maxdepth 1 -type f -name '*.txt' -print0 | sort -zV)

    index=$(<dailyIndexFile)
    echo "Starting pinocchio with: ${files[index]}"
    ((index++))
    index=$((index % ${#files[@]}))
    echo "$index" > dailyIndexFile

    # Execute pinocchio.py with the next file
    python3 "/home/meulindux/AutostockUtils/Utils/multiPinocchio.py" "${files[index]}"
else
    echo "Not running because it's before 8 AM."
fi
