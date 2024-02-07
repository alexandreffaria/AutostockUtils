#!/bin/bash

# Path to the folder containing the files (assuming it's in the same directory as the script)
folder="$(dirname "$0")/Prompts"
# Path to the file storing the last used file
index_file="$folder/dailyIndexFile"

# Check if the directory exists and contains files
if [ ! -d "$folder" ] || [ -z "$(ls -A "$folder")" ]; then
    echo "Error: '$folder' directory doesn't exist or is empty."
    exit 1
fi

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
next_index=$((index % ${#files[@]}))

# Get the next file using the calculated index
next_file="${files[next_index]}"

echo "python3 pinocchio.py Prompts/$next_file"

# Execute pinocchio.py with the next file
python3 "pinocchio.py" "$folder/$next_file"

# Update the index file with the next index
next_index=$(( (index + 1) % ${#files[@]} ))
echo "$next_index" > "$index_file"
