import sys, os

def processFolder(folderPath):
    print("Process Folder")
    for root, dirs, files in os.walk(folderPath):
        for fileName in files:
            if fileName.endswith(".txt"):
                filePath = os.path.join(root, fileName)
                print(filePath)
                removeDuplicates(filePath)

def removeDuplicates(promptsFile):
    uniquePrompts = set()
    with open(promptsFile, "r") as prompts:
        for prompt in prompts:
            uniquePrompts.add(prompt.strip().replace('"', ''))
    
    sortedPrompts = sorted(uniquePrompts)

    with open (promptsFile, "w") as output:
        for uniquePrompt in sortedPrompts:
            output.write(uniquePrompt + "\n")

        print("Duplicates have being, hopefully, successfully removed")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rmDupPrompts.py <prompts.txt> [-f <folder>]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        removeDuplicates(sys.argv[1])
    elif len(sys.argv) == 3 and sys.argv[1] == "-f":
        processFolder(f"{sys.argv[2]}")
