from datetime import datetime
import pandas as pd
from fuzzywuzzy import process, fuzz

# Load the CSV file into a DataFrame
df_items = pd.read_csv('items_20240708_031709.csv')
df_labels = pd.read_csv('top_labels_20240708231535.csv')
print(df_labels)
# Create a list of labels to check
labels_to_check = df_labels['Label'].tolist()

# Strip all spaces from the beginning and end of the Description column
df_items['Description'] = df_items['Description'].str.strip()

# Filter df1 based on whether the Description contains any of the labels in df2
filtered_df_items = df_items[df_items['Description'].apply(lambda desc: any(label in desc.lower() for label in labels_to_check))]
sorted_filtered_df_items = filtered_df_items.sort_values(by='Description').reset_index(drop=True)
# print(sorted_filtered_df_items)

# Create a timestamp
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

# Define the filename
filename = f'filtered_items_{timestamp}.csv'

# Save DataFrame to CSV
# sorted_filtered_df_items.to_csv(filename, index=False)

print(f'DataFrame saved to {filename}')

# Function to find similar entries and keep only one
def find_and_remove_similar(df, threshold=90):
    # Calculate similarity for each pair of descriptions
    duplicates = []
    for i, desc1 in enumerate(df['Description']):
        for j, desc2 in enumerate(df['Description']):
            if i != j and fuzz.ratio(desc1, desc2) >= threshold:
                duplicates.append(desc2)

    # Drop the duplicate entries
    sorted_filtered_df_items.drop_duplicates(subset='Description', inplace=True)

# Find and remove similar entries
find_and_remove_similar(sorted_filtered_df_items)

print(sorted_filtered_df_items)