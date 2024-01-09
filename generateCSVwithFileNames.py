import os
import csv
import argparse


def create_csv(folder_path):
    # Get a list of all files in the specified folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Create a CSV file and write the header
    with open("output.csv", "w", newline="") as csvfile:
        fieldnames = ["Filename", "Title", "Keywords", "Category", "Releases"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Dictionary to store title and keywords for each unique filename
        filename_info = {}

        current_file_count = 0  # Counter for unique filenames

        for file in files:
            # Process each unique filename
            filename_base = (
                file.split("_", 1)[-1].rsplit("_", 1)[0].replace("_", " ")
                if "_" in file
                else file
            )
            if filename_base not in filename_info:
                # Increment the counter for unique filenames
                current_file_count += 1

                # Prompt for title, keywords, and category for each unique filename
                title = input(
                    f"({current_file_count}/{len(set(files))}) Enter title for {filename_base}: "
                )
                keywords = input(
                    f"({current_file_count}/{len(set(files))}) Enter keywords (comma separated) for {filename_base}: "
                )
                category = input(
                    f"({current_file_count}/{len(set(files))}) Enter category for {filename_base}: "
                )

                # Remove leading and trailing whitespaces
                title = title.strip()
                keywords = keywords.strip()
                category = category.strip()

                # Enclose keywords in double quotes
                keywords = f"{keywords}"

                # Store title, keywords, and category for the unique filename
                filename_info[filename_base] = {
                    "Title": title,
                    "Keywords": keywords,
                    "Category": category,
                }

            # Write the information to the CSV file for the current file
            writer.writerow(
                {
                    "Filename": file,
                    "Title": filename_info[filename_base]["Title"],
                    "Keywords": filename_info[filename_base]["Keywords"],
                    "Category": filename_info[filename_base]["Category"],
                    "Releases": "",
                }
            )

            print(
                f"({current_file_count}/{len(set(files))}) Information for {file} written to CSV."
            )

    print(f'CSV file created successfully: {os.path.abspath("output.csv")}')
    print(f"Processing complete. {len(set(files))} unique files processed.")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Create a CSV file with filenames from a specified folder."
    )
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing files."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to create the CSV file
    create_csv(args.folder_path)
