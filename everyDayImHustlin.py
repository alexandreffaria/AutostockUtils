import os

# Function to read the daily index from the file
def read_daily_index():
    with open("dailyIndexFile", "r") as f:
        return int(f.read().strip())

# Function to write the updated daily index to the file
def write_daily_index(index):
    with open("dailyIndexFile", "w") as f:
        f.write(str(index))

# Function to execute the command
def execute_command(prompt_file):
    os.system(f"python3 Utils/pinocchio.py {prompt_file}")

# Main function
def main():
    # Read daily index
    daily_index = read_daily_index()

    # Get list of files in the Prompts folder
    prompt_files = os.listdir(r"\\wsl.localhost\Ubuntu-22.04\home\meulindux\AutostockUtils/Prompts")

    # Check if there are any prompt files
    if prompt_files:
        # Get the index modulo the number of prompt files to ensure it wraps around
        chosen_index = daily_index % len(prompt_files)
        chosen_prompt_file = prompt_files[chosen_index]
        
        # Execute the command
        execute_command(f"/Prompts/{chosen_prompt_file}")

        # Increment index
        daily_index += 1

        # Write updated index
        write_daily_index(daily_index)
    else:
        print("No prompt files found in the Prompts folder.")

if __name__ == "__main__":
    main()
