import sqlite3
import re
import sys

def parse_line(line):
    parts = line.split("\t")

    date = parts[0].split(', ')[0]
    time = parts[0].split(', ')[1]
    id_str = parts[2]
    license = parts[3]
    royalty_str = parts[4].replace('US$', '').replace(',', '.')
    royalty = float(royalty_str)

    return date, time, id_str, license, royalty


def main(file_path):
    connection = sqlite3.connect('./Stats/Data/sales_data.db')
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS royalties (
            date TEXT,
            time TEXT,
            id INTEGER,
            license TEXT,
            royalty REAL,
            UNIQUE(date, id)
        )
    ''')

    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip the header
        for line in file:
            data = parse_line(line)
            try:
                cursor.execute('INSERT OR IGNORE INTO royalties (date, time, id, license, royalty) VALUES (?, ?, ?, ?, ?)', data)
            except sqlite3.Error as e:
                print(f"An error occurred: {e.args[0]}")

    connection.commit()
    connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python insertAdobeIntoDatabase.py <path_to_txt_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)