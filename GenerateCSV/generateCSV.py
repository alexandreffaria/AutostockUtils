import os, csv, argparse
from gptApi import *

prompts_folder_path = "Prompts"
prompts_extension = ".txt"


def find_prompt_for_filename(filename_base, prompts_folder_path):
    # Loop over the directory tree
    for root, _, files in os.walk(prompts_folder_path):
        # Loop over files in the current directory
        for filename in files:
            if filename.endswith(".txt"):
                prompts_file_path = os.path.join(root, filename)

                # Read prompts from the file
                with open(prompts_file_path, "r") as prompts_file:
                    prompts = prompts_file.read().split("\n")

                # Search for the prompt containing the unique part of the filename
                for prompt in prompts:
                    if filename_base in prompt.replace(",", "").replace(
                        ".", ""
                    ).replace("'", ""):
                        print("FOUND")
                        return prompt.strip()
    print("NOT FOUND")


def create_csv(folder_path, category, prompts_file_path):
    parent_folder_name = os.path.basename(
        os.path.normpath(os.path.join(folder_path, ".."))
    )

    # Get a list of all files in the specified folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    csv_file_name = f"{parent_folder_name}_output.csv"

    # Create a CSV file and write the header
    with open(csv_file_name, "w", newline="") as csvfile:
        fieldnames = ["Filename", "Title", "Keywords", "Category", "Releases"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Dictionary to store title and keywords for each unique filename
        filename_info = {}

        current_file_count = 0  # Counter for unique filenames

        for file in files:
            # Process each unique filename
            filename_base = (
                file[8:63].rsplit("_", 1)[0].replace("_", " ")
                if "_" in file[63:]
                else file[63:]
            )

            if filename_base not in filename_info:
                # Increment the counter for unique filenames
                current_file_count += 1
                fullPrompt = find_prompt_for_filename(
                    filename_base.strip(), prompts_file_path
                )
                # Prompt for title, keywords, and category for each unique filename

                gptTitle = createTitle(fullPrompt, "pt")
                gptTitle = gptTitle.replace(",", "").replace(".", "").replace("'", "")

                gptKeywords = getKeywords(gptTitle, "pt")

                # Remove leading and trailing whitespaces
                gptTitle = gptTitle.strip()
                gptTitle = gptTitle.strip("\n")
                gptTitle = gptTitle.strip(",")
                gptKeywords = gptKeywords.strip(".")
                gptKeywords = gptKeywords.strip("\n")

                # Enclose keywords in double quotes
                gptKeywords = f"{gptKeywords}"

                # Store title, keywords, and category for the unique filename
                filename_info[filename_base] = {
                    "Title": gptTitle,
                    "Keywords": gptKeywords,
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

            print(f"{file} | written to CSV.")

    print(f"CSV file created successfully: {os.path.abspath(csv_file_name)}")
    print(f"Processing complete. {len(set(files))} unique files processed.")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Create a CSV file with filenames from a specified folder. python generateCSV.py /path of images/ --category {1..21}"
    )
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing files."
    )
    parser.add_argument("--category", type=int, help="Category of the images.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Get the prompts file path based on the provided category
    prompts_file_path = "promptGeneratorOutput/"

    # Call the function to create the CSV file
    create_csv(args.folder_path, args.category, prompts_file_path)
