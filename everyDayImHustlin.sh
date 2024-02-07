#!/bin/bash

# Specify the folder path
folder="Prompts"
files=()

# Loop through each file in the folder, sorted numerically
while IFS= read -r -d '' file; do
    # Check if the file is a regular file (not a directory)
    if [ -f "$file" ]; then
        files+=("$file") # Add the file to the array
    fi
done < <(find "$folder" -maxdepth 1 -type f -name '*.txt' -print0 | sort -zV)

# Process the files in the array
for file in "${files[@]}"; do
    echo "Processing file: $file"
    # Add your processing logic here
done

index=$(<dailyIndexFile)
echo "Starting pinocchio with: ${files[index]}"
((index++))
index=$((index % ${#files[@]}))
echo "$index" > dailyIndexFile
# # Execute pinocchio.py with the next file
python3 "pinocchio.py" "${files[index]}"
