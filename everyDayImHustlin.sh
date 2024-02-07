#!/bin/bash

# Specify the folder path
folder="/home/meulindux/Desktop/AutostockUtils/Prompts"
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
# # Execute pinocchio.py with the next file
python3 "pinocchio.py" "${files[index]}"
