import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import seaborn as sns

# File path
input_file = 'weeklyEarning-08-23_07-24_treated.csv'

# Load the data
df = pd.read_csv(input_file)

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# Sort data by date
df = df.sort_values('Date')

# Basic Statistics
mean_value = df['Amount'].mean()
std_dev = df['Amount'].std()
median_value = df['Amount'].median()
total_sum = df['Amount'].sum()

print("Basic Statistics:")
print(f"Mean: {mean_value:.2f}")
print(f"Standard Deviation: {std_dev:.2f}")
print(f"Median: {median_value:.2f}")
print(f"Total Sum: {total_sum:.2f}\n")

# Time Series Plot
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Amount'], marker='o', linestyle='-', color='b', label='Daily Earnings')
plt.title('Daily Earnings Over Time')
plt.xlabel('Date')
plt.ylabel('Amount (US$)')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('time_series_plot.png')
plt.show()

# Scatter Plot with Linear Regression
slope, intercept, r_value, p_value, std_err = linregress(df.index, df['Amount'])
df['Trend'] = intercept + slope * df.index

plt.figure(figsize=(10, 5))
sns.regplot(x=df.index, y=df['Amount'], color='blue', marker='o', line_kws={'color': 'red'})
plt.title('Scatter Plot with Trend Line')
plt.xlabel('Date Index')
plt.ylabel('Amount (US$)')
plt.grid(True)
plt.tight_layout()
plt.savefig('scatter_with_trend.png')
plt.show()

print("Regression Statistics:")
print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"R-squared: {r_value**2:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Standard Error: {std_err:.4f}\n")

# Plot with Trend Line
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Amount'], marker='o', linestyle='-', color='b', label='Daily Earnings')
plt.plot(df['Date'], df['Trend'], color='r', linestyle='-', label='Trend Line')
plt.title('Daily Earnings with Trend Line')
plt.xlabel('Date')
plt.ylabel('Amount (US$)')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('trend_line_plot.png')
plt.show()

# Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df['Amount'], bins=20, kde=True)
plt.title('Distribution of Daily Earnings')
plt.xlabel('Amount (US$)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.savefig('distribution_plot.png')
plt.show()

# Box Plot
plt.figure(figsize=(8, 5))
sns.boxplot(x=df['Amount'])
plt.title('Box Plot of Daily Earnings')
plt.xlabel('Amount (US$)')
plt.grid(True)
plt.tight_layout()
plt.savefig('box_plot.png')
plt.show()

# Moving Average
window_size = 30  # Example window size for weekly moving average
df['Moving Average'] = df['Amount'].rolling(window=window_size).mean()

plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Amount'], marker='o', linestyle='-', color='b', label='Daily Earnings')
plt.plot(df['Date'], df['Moving Average'], color='r', linestyle='-', label=f'{window_size}-day Moving Average')
plt.title(f'Daily Earnings with {window_size}-day Moving Average')
plt.xlabel('Date')
plt.ylabel('Amount (US$)')
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('moving_average_plot.png')
plt.show()
