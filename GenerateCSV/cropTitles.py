import csv
import re
import sys
import os


def crop_title(title, max_length=200):
    phrases = re.findall("[A-Z][^A-Z]*", title)
    cropped_title = ""
    current_length = 0

    for phrase in phrases:
        phrase_length = len(phrase)
        if current_length + phrase_length > max_length:
            # Find the last space within the limit
            last_space_index = cropped_title.rfind(" ", 0, max_length)
            if last_space_index != -1:
                cropped_title = cropped_title[:last_space_index]
            break
        else:
            if current_length > 0:
                cropped_title += " "
            cropped_title += phrase
            current_length += phrase_length

    return cropped_title.strip()


def process_csv(input_file):
    with open(input_file, "r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames

        output_file_name, output_file_extension = os.path.splitext(input_file)
        output_file_name += "_cropped_titles"
        output_csv_file = output_file_name + output_file_extension

        with open(output_csv_file, "w", encoding="utf-8", newline="") as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                title = row["Title"]
                cropped_title = crop_title(title)
                row["Title"] = cropped_title
                writer.writerow(row)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.csv")
        sys.exit(1)

    input_csv_file = sys.argv[1]

    process_csv(input_csv_file)
