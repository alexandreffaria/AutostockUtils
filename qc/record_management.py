import os
import csv
import logging
from typing import Dict

from constants import MASTER_CSV

def read_record_file(record_file_path: str) -> Dict[str, str]:
    """Read the record file and return a dictionary of {file_name: action}."""
    records = {}
    if os.path.exists(record_file_path):
        try:
            with open(record_file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                records = {row[0].strip(): row[1].strip() for row in reader if len(row) == 2}
        except Exception as e:
            logging.error(f"Error reading record file: {e}")
    return records

def write_record_file(record_entries: Dict[str, str], record_file_path: str) -> None:
    """Write the record entries to the record file."""
    try:
        # Merge with existing records
        existing_records = read_record_file(record_file_path)
        existing_records.update(record_entries)
        with open(record_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for file_name, action in existing_records.items():
                writer.writerow([file_name, action])
        logging.info("Record file updated.")
    except Exception as e:
        logging.error(f"Error writing record file: {e}")

def merge_records_to_master_csv(folder_path: str, new_records: Dict[str, str]) -> None:
    """Merge new records into the master CSV file."""
    master_csv_path = os.path.join(os.path.dirname(folder_path), MASTER_CSV)
    
    existing_records = {}
    if os.path.exists(master_csv_path):
        with open(master_csv_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            existing_records = {row[0]: row[1] for row in reader}
    
    existing_records.update(new_records)
    
    with open(master_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for file_name, action in existing_records.items():
            writer.writerow([file_name, action])
    
    logging.info(f"Records merged into master CSV: {master_csv_path}")