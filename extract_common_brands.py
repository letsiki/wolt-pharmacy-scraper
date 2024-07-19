import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re
import csv
from datetime import datetime
from data.input.excluded_words import EXCLUDED_WORDS

# Load the CSV file into a DataFrame
df = pd.read_csv('data/output/items_20240708_031709.csv')

# Initialize a Counter dict
word_counter = Counter()

# Define a set of common measurement abbreviations to exclude
measurement_units = {'cm', 'mm', 'kg', 'g', 'mg', 'l', 'ml', 'm', 'km', 'ft', 'in', 'yd', 'oz', 'lb'}

# Filtering function to exclude unwanted words
def is_valid_word(word, invalid_strings=None):
    if invalid_strings is None:
        invalid_strings = []
    # Check if the word is numeric
    if word.isnumeric():
        return False
    # Check if the word is a single letter or single symbol
    if len(word) == 1:
        return False
    # Check if the word is a measurement unit
    if word in measurement_units:
        return False
    # Check if the word contains only special characters
    if re.match(r'^[^\w\s]+$', word):
        return False
    # Check if the word is in the invalid strings list
    if word in invalid_strings:
        return False
    # Check if the word is a numeric value followed by a measurement unit
    if re.match(r'^\d+(cm|mm|kg|g|mg|l|ml|m|km|ft|in|yd|oz|lb)$', word):
        return False
    return True

# Iterate over each row in the first column
for row in df.iloc[:, 0]:
    # Split the string into words, convert to lower case and filter them
    words = row.lower().split()
    filtered_words = [word for word in words if is_valid_word(word, EXCLUDED_WORDS)]
    word_counter.update(filtered_words)

# Get a list of (word, count) sorted by count in descending order
sorted_word_counts = word_counter.most_common(50)  # Get only the top 50 words


# Print the sorted word counts
for word, count in sorted_word_counts:
    print(f'\'{word}\'', end=', ')


# Extract words and counts for visualization
words, counts = zip(*sorted_word_counts)

# Create a bar plot for visualization
plt.figure(figsize=(14, 8))
plt.bar(words, counts)
plt.xlabel('Words')
plt.ylabel('Counts')
plt.title('Top 50 Word Frequency')
plt.xticks(rotation=90)
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
plt.show()

# # Prepare data for the pie chart
# top_n = 10
# top_words = sorted_word_counts[:top_n]
# other_words = sorted_word_counts[top_n:]

# # Calculate the total counts
# total_count = sum(word_counter.values())
# top_count = sum(count for _, count in top_words)
# other_count = total_count - top_count

# # Data for the pie chart
# labels = [word for word, _ in top_words] + ['Others']
# sizes = [count for _, count in top_words] + [other_count]

# # Create a pie chart
# plt.figure(figsize=(10, 6))
# plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
# plt.title(f'Top {top_n} Words and Others')
# plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.show()

# Function to write top labels to a CSV file
def write_top_labels_to_csv(top_n):
    # Get the top_n words
    top_words = sorted_word_counts[:top_n]

    # Prepare the data for the CSV file
    labels = [word for word, _ in top_words]

    # Create a timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Define the filename
    filename = f'data/output/top_labels_{timestamp}.csv'

    # Write to the CSV file
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Label'])
        # Write the labels
        for label in labels:
            writer.writerow([label])

    print(f'CSV file "{filename}" has been created successfully.')

# Example usage of the function
write_top_labels_to_csv(50)  # Pass the desired number of top words to include