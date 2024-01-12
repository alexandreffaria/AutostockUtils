import os, csv, argparse, subprocess
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = api_key

client = OpenAI()

gptModel = "gpt-3.5-turbo-1106"
# gptmodel = "gpt-4"
prompts_file_path = "prompts.txt"

def find_prompt_for_filename(filename_base):
    # Read prompts from the file
    print(filename_base)
    with open(prompts_file_path, "r") as prompts_file:
        prompts = prompts_file.read().split('\n')
    
    # Search for the prompt containing the unique part of the filename
    for prompt in prompts:
        if filename_base.lower().strip("\',") in prompt.lower():
            print("FOUND")
            return prompt.strip()
    print("NOT FOUND")
    return None

def getGPTResponse(model, role, content):
    gptPrompt = [
        {"role": "system", "content": "You are an award-winning director of photography specialized in stock photography."},
        {"role": role, "content": content},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=gptPrompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content.strip()

def get_category():
    # Prompt the user for the category
    category = input("Enter the category for all files: ")
    return category


def translate_title(title):
    gptTitle = getGPTResponse(gptModel, "user", f"I'm going to give you a title in English and you should translate it to Portuguese, the title should not be longer than 200 letters! \n\n {title} \n just give me the translation with no other information in your response. Don't use any pontualtion like (',.-!)")
    return gptTitle


def getKeywords(title):
    gptKeywords = getGPTResponse(gptModel, "user", f"Me dê 30 palavras chaves que sejam relacionadas ao seguinte título de uma imagem: \n{title}\nOrganize as palavras chave por ordem de relevância, e nunca utilize palavras genéricas como 'imagem', ou 'cena'.\nTodas as palavras chave devem ser separadas por vírgulas\nJust give me the keywords in portuguese with no other information in your response.\nHere is an example:")
    return gptKeywords

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
        category = get_category()

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
                fullPrompt = find_prompt_for_filename(filename_base.strip())
                # Prompt for title, keywords, and category for each unique filename
                
                gptTitle = translate_title(fullPrompt)
                gptTitle = gptTitle.replace(',', '').replace('.', '')

                gptKeywords = getKeywords(gptTitle)
                category = category.strip()

                # Remove leading and trailing whitespaces
                gptTitle = gptTitle.strip()
                gptTitle = gptTitle.strip("\n")
                gptTitle = gptTitle.strip(",")
                gptKeywords = gptKeywords.strip(".")
                gptKeywords = gptKeywords.strip("\n")
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
                    "Title": filename_info[filename_base]["Title"].strip('",.-'),
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
        description="Create a CSV file with filenames from a specified folder."
    )
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing files."
    )

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to create the CSV file
    create_csv(args.folder_path)
