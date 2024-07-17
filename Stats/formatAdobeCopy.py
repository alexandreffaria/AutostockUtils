import re
from datetime import datetime

# Define month translations from Portuguese to English
months = {
    'janeiro': 'January', 'fevereiro': 'February', 'março': 'March',
    'abril': 'April', 'maio': 'May', 'junho': 'June',
    'julho': 'July', 'agosto': 'August', 'setembro': 'September',
    'outubro': 'October', 'novembro': 'November', 'dezembro': 'December'
}

# Initialize an empty dictionary
daily_earnings = {}

input_file = "Stats/Data/jun24-jul24.txt"

# Read the data from the file
with open(input_file, 'r', encoding='utf-8') as data:
    for line in data:
        # Split the line into date and value based on the tab character
        date_str, value = line.strip().split('\t')

        # Extract day, month, and year using regex
        match = re.match(r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', date_str)
        if match:
            day, month_str, year = match.groups()
            # Convert Portuguese month to English month
            month = months[month_str.lower()]
            # Convert to datetime object and then to the desired format
            date_num = datetime.strptime(f"{day} {month} {year}", "%d %B %Y").strftime("%d/%m/%Y")

            # Convert value to float
            value = float(value.replace('US$ ', '').replace(',', '.'))

            # Add to the dictionary
            daily_earnings[date_num] = value

# Print the dictionary
print(daily_earnings)

output_file = f"{input_file[:-4]}_treated.csv"

# Write the processed data to the output file
with open(output_file, 'w', encoding='utf-8') as output:
    output.write("Date,Amount\n")
    for date, earnings in reversed(daily_earnings.items()):
        output.write(f"{date},{earnings:.2f}\n")

# Print a confirmation message
print(f"Processed data has been written to {output_file}")