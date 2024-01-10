import os, csv, argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key

client = OpenAI()

gptModel = "gpt-3.5-turbo-1106"
# gptmodel = "gpt-4"


def translate_title(title):
    # Use GPT-4 to translate the title

    gptPrompt = [
        {
            "role": "system",
            "content": "You are an award-winning director of photography specialized in stock photography.",
        },
        {
            "role": "user",
            "content": f"I'm going to give you a title in English and you should translate it to Portuguese, the title should not be longer than 200 letters! \n\n {title}",
        },
    ]

    response = client.chat.completions.create(
        model=gptModel,
        messages=gptPrompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract the translated text from the GPT-4 response
    gptAwnser = response.choices[0].message.content

    return gptAwnser


def getKeywords(title):
    gptPrompt = [
        {
            "role": "system",
            "content": "You are an award-winning director of photography specialized in stock photography.",
        },
        {
            "role": "user",
            "content": f"Me dê 30 palavras chaves que sejam relacionadas ao seguinte título de uma imagem: \n\n {title} \n\n Organize as palavras chave por ordem de relevância, e não utilize palavras genéricas como 'imagem', ou 'cena'. Todas as palavras chave devem ser separadas por vírgulas e sem espaços e sem pontos finais",
        },
    ]

    response = client.chat.completions.create(
        model=gptModel,
        messages=gptPrompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Extract the translated text from the GPT-4 response
    gptAwnser = response.choices[0].message.content

    return gptAwnser


def create_csv(folder_path):
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
                gptTitle = translate_title(title)

                gptKeywords = getKeywords(gptTitle)

                category = input(
                    f"({current_file_count}/{len(set(files))}) Enter category for {filename_base}: "
                )

                # Remove leading and trailing whitespaces
                gptTitle = gptTitle.strip()
                gptKeywords = gptKeywords.strip(".")
                category = category.strip()

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

            print(
                f"({current_file_count}/{len(set(files))}) Information for {file} written to CSV."
            )

    print(f"CSV file created successfully: {os.path.abspath(csv_file_name)}")
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
