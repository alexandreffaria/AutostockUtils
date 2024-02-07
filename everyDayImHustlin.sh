#!/bin/bash

# Path to the folder containing the files
folder="/Prompts"
# Path to the file storing the last used file
index_file="/Prompts/dailyIndexFile"

# Check if the index file exists
if [ -f "$index_file" ]; then
    # Read the index from the file
    index=$(<"$index_file")
else
    # If the index file doesn't exist, start from the first file
    index=0
fi

# Get the list of files sorted by name
files=($(ls -1 "$folder" | sort))

# Calculate the index of the next file
next_index=$(( (index + 1) % ${#files[@]} ))

# Get the next file using the calculated index
next_file="${files[next_index]}"

# Execute pinocchio.py with the next file
python3 "pinocchio.py" "$folder/$next_file"

# Update the index file with the next index
echo "$next_index" > "$index_file"
