import csv
import re
import sys
import os
import glob
import shutil

# Define a function to remove non-alphanumeric characters except commas, double quotes, and replace dashes with spaces
def clean_text(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9," -]', '', text)  # Remove non-alphanumeric characters except commas, double quotes, spaces, and dashes
    cleaned_text = cleaned_text.replace('-', ' ')  # Replace dashes with spaces
    return cleaned_text

if __name__ == "__main__":
    # Check if a folder path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    # Get the folder path from command-line arguments
    folder_path = sys.argv[1]

    try:
        # Get the list of CSV files in the specified folder
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))
        
        # Ensure there's exactly one CSV file in the folder
        if len(csv_files) != 1:
            print("Error: There should be exactly one CSV file in the folder.")
            sys.exit(1)
        
        # Get the file path of the CSV file
        file_path = csv_files[0]

        # Construct the temporary file path
        temp_file_path = os.path.splitext(file_path)[0] + '_temp.csv'

        with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
             open(temp_file_path, 'w', newline='', encoding='utf-8') as outfile:

            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Apply the function to the 'Title' and 'Keywords' columns
                row['Title'] = clean_text(row.get('Title', ''))
                row['Keywords'] = clean_text(row.get('Keywords', ''))

                # Write the modified row to the temporary file
                writer.writerow(row)

        # Replace the original CSV file with the cleaned version
        shutil.move(temp_file_path, file_path)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
