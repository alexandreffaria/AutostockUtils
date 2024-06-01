# Get the directory containing the script file
$scriptDirectory = $PSScriptRoot

# Specify the relative path to the Prompts folder
$promptsPath = Join-Path -Path $scriptDirectory -ChildPath "Prompts\"

# Get the list of prompt files
$promptsFiles = Get-ChildItem -Path $promptsPath -File | 
                Select-Object -ExpandProperty Name |
                Sort-Object {[int]($_ -replace '\D','')}

# Read the daily index from the file
$dailyIndexFilePath = Join-Path -Path $scriptDirectory -ChildPath "dailyIndexFile"
$dailyIndex = [int](Get-Content -Path $dailyIndexFilePath)

# Calculate the index for the day's prompt
$arrayIndex = $dailyIndex - 1
$dayPrompt = $promptsFiles[$arrayIndex]

# Construct the full path to the day's prompt
$dayFullPath = Join-Path -Path $scriptDirectory -ChildPath ("Prompts\" + $dayPrompt)

# Execute the Python script with the day's prompt
Start-Process python -ArgumentList "$scriptDirectory\Utils\pinocchio.py", $dayFullPath -Wait:$false

# Calculate the new daily index
$newDailyIndex = ($dailyIndex % 21) + 1

# Update the daily index file
Set-Content -Path $dailyIndexFilePath -Value $newDailyIndex

