import os
import csv
import argparse
from gptApi import *
from tqdm import tqdm

prompts_folder_path = "/home/meulindux/AutostockUtils/promptGeneratorOutput/"


def find_matching_prompt(input_string):
    matching_prompt = None

    # Loop over the directory tree
    for root, _, files in os.walk(prompts_folder_path):
        # Loop over files in the current directory
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)

                # Read the content of the file
                with open(file_path, "r") as file:
                    content = file.read().split("\n")

                # Search for the matching string within the file content
                for line in content:
                    if input_string.lower() in line.lower():
                        matching_prompt = line.strip()
                        break
                if matching_prompt:
                    break
        if matching_prompt:
            break

    return matching_prompt


def create_csv(input_csv_file):
    filename = 0
    title = 1
    keywords = 3
    license = 4

    output_csv_file = os.path.splitext(input_csv_file)[0] + "_output.csv"

    with open(input_csv_file, "r", newline="") as csvTemplate, open(
        output_csv_file, "w", newline=""
    ) as csvOutput:

        csvReader = csv.reader(csvTemplate)
        csvWriter = csv.writer(csvOutput)

        header = next(csvReader)
        csvWriter.writerow(header)

        # Get the total number of rows in the CSV file
        num_rows = sum(1 for row in csv.reader(open(input_csv_file)))

        for row in tqdm(csvReader, total=num_rows - 1, desc="Processing CSV"):
            file = row[filename]

            baseName = (
                file[8:63].rsplit("_", 1)[0].replace("_", " ")
                if "_" in file[63:]
                else file[63:]
            )

            fullPrompt = find_matching_prompt(baseName.strip())
            gptTitle = createTitle(fullPrompt, "en").replace(
                ",", ""
            ).replace(
                ".", ""
            ).replace(
                "'", ""
            ).strip(
                "\n"
            ).strip()
            gptKeywords = getKeywords(gptTitle, "en")
            gptKeywords = f"{gptKeywords}"

            row[title] = f"AI generated {gptTitle}"
            row[keywords] = f"ai generated, {gptKeywords}"
            row[license] = "free"

            csvWriter.writerow(row)

    return output_csv_file


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Change the CSV file with filenames. python generateCSV.py /pathToCsv/"
    )
    parser.add_argument(
        "input_csv_file", type=str, help="Path to the input csv file."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to create the new CSV file
    output_csv_file = create_csv(args.input_csv_file)
    print(f"New CSV file created: {output_csv_file}")
