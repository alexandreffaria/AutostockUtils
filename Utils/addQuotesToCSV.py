import csv
import sys

def add_quotes_to_fields_excluding_header(file_path):
    # Read the original content
    with open(file_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')
        rows = list(reader)
    
    # Open the file in write mode to overwrite it
    with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        
        if rows:
            # Write the header without quotes
            writer.writerow(rows[0])
            
            # Write the remaining rows with quotes added by the csv module
            for row in rows[1:]:
                writer.writerow(row)

            # Now, read the first line again and remove quotes from it
    with open(file_path, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        
        # Remove quotes from the first line
        if lines:
            header = lines[0].replace('"', '')
            lines[0] = header
        
        # Write the modified lines back to the file
        file.seek(0)
        file.writelines(lines)
        file.truncate()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quote_csv_fields.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]

    # Confirm the action to the user
    print(f"Modifying the file in place: {file_path}")

    add_quotes_to_fields_excluding_header(file_path)

    print(f"Quoted fields updated in {file_path}")
