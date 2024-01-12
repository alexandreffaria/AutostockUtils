import sys

def remove_first_two_quotes(line):
    """
    Removes the first two double quotation marks from a given line.
    """
    return line.replace('"', '', 2)

def process_file(file_path):
    """
    Reads a file line by line, removes the first two double quotation marks,
    and overwrites the input file with the modified lines.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            modified_line = remove_first_two_quotes(line)
            file.write(modified_line)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]

    process_file(input_file_path)
