import pandas as pd
import re
import sys
import os

# Define a function to remove non-alphanumeric characters except commas and double quotes
def remove_non_alphanumeric_except_commas_and_quotes(text):
    return re.sub(r'[^\w\s,]', '', text)

if __name__ == "__main__":
    # Check if a file path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)

    # Get the file path from command-line arguments
    file_path = sys.argv[1]

    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Apply the function to the 'Title' and 'Keywords' columns
        df['Title'] = df['Title'].apply(remove_non_alphanumeric_except_commas_and_quotes)
        df['Keywords'] = df['Keywords'].apply(remove_non_alphanumeric_except_commas_and_quotes)

        # Construct the output file path
        output_file_path = os.path.splitext(file_path)[0] + '_nonAlpha.csv'

        # Write the modified DataFrame back to CSV
        df.to_csv(output_file_path, index=False)
        print(f"Cleaned data saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
