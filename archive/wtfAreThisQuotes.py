import sys

def processQuote(line):
    parts = line.split(',')

    parts[1] = parts[1].strip('"')

    for part in parts:
        print(part)
    


    return ''.join(parts)

def parseQuotes(file_name):
    with open(file_name, 'r') as f:
        for line in f:
            processQuote(line)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        parseQuotes(file_name)
    else:
        print('Please provide a file name.')
