import csv
import sys
import os

def add_quotes_to_fields_in_place(file_path):
    # Read the original content
    with open(file_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        rows = [row for row in reader]

    # Write back with quotes added around each field
    with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quote_csv_fields.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]

    # Confirm the action to the user
    print(f"Modifying the file in place: {file_path}")

    add_quotes_to_fields_in_place(file_path)

    print(f"Quoted fields updated in {file_path}")
