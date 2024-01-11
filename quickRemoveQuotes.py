input_file = "011124_Mental_Health_output.csv"  # Replace with your actual CSV file name
output_file = "modified_csv_file.csv"  # Replace with the desired output file name


def remove_quotes_and_commas_from_title(line):
    # Check if the line is not empty or contains only whitespace
    if line.strip():
        # Initialize variables for quotes and commas
        quote_count = 0
        comma_between_quotes = False

        # Process each character in the line
        i = 0
        while i < len(line):
            char = line[i]

            # If the character is a double quote, remove it
            if char == '"':
                quote_count += 1
                if quote_count <= 2:
                    line = line[:i] + line[i + 1 :]
                    if quote_count == 2:
                        comma_between_quotes = (
                            False  # Reset flag after the second quote
                        )
                else:
                    i += 1  # Skip to the next character after the second quote
            # If the character is a comma between the first and second quotes, remove it
            elif char == "," and quote_count == 1:
                line = line[:i] + line[i + 1 :]
                comma_between_quotes = True
            else:
                i += 1

        # If there was a comma between the quotes, add a space after the second quote
        if comma_between_quotes:
            line = line.replace('"', '" ')

        # Write the modified line to the output file
        return line

    return line


# Read the input file and write the modified data to the output file
with open(input_file, "r", encoding="utf-8") as infile, open(
    output_file, "w", encoding="utf-8"
) as outfile:
    first_line = infile.readline()
    outfile.write(first_line)  # Write the first line as it is

    for line in infile:
        # Remove double quotes and commas from the "Title" column in each line
        modified_line = remove_quotes_and_commas_from_title(line)

        # Write the modified line to the new CSV file
        outfile.write(modified_line)

print(f"Titles without double quotes and commas have been saved to {output_file}")
