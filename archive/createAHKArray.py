import sys
import os


def generate_function_file(input_file):
    output_file = f"{os.path.splitext(input_file)[0]}_modified.txt"
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        # Write the first line outside of the array
        first_line = infile.readline().strip()
        if first_line:
            outfile.write(f'PromptArray := ["{first_line}"]\n')
        # Write PromptArray.Push lines for each subsequent line
        for line in infile:
            line = line.strip()
            if line:
                outfile.write(f'PromptArray.Push("{line}")\n')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
    else:
        input_file = sys.argv[1]
        generate_function_file(input_file)
