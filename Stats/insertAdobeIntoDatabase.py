import sqlite3
import re
import sys

def parse_line(line):
    parts = re.split(r'\s\s+', line.strip())
    if len(parts) < 4:
        return None
    timestamp, id_str, license, royalty_str = parts
    royalty = float(royalty_str.replace('US$', '').replace(',', '.'))
    date, time = timestamp.split(', ')
    return date, time, id_str, license, royalty

def main(file_path):
    connection = sqlite3.connect('sales_data.db')
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
            if data := parse_line(line):
                cursor.execute('INSERT OR IGNORE INTO royalties (date, time, id, license, royalty) VALUES (?, ?, ?, ?, ?)', data)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python insertAdobeIntoDatabase.py <path_to_txt_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)