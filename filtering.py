from datetime import datetime
from multiprocessing import Pool, cpu_count, freeze_support
import pandas as pd
from Levenshtein import ratio as levenshtein_ratio

# Load the CSV file into a DataFrame
df_items = pd.read_csv('data/items_20240708_031709.csv')
df_labels = pd.read_csv('data/top_labels_20240708231535.csv')
# print(df_labels)
# Create a list of labels to check
labels_to_check = df_labels['Label'].tolist()

# Strip all spaces from the beginning and end of the Description column
df_items['Description'] = df_items['Description'].str.strip()

# Filter df1 based on whether the Description contains any of the labels in df2
filtered_df_items = df_items[df_items['Description'].apply(lambda desc: any(label in desc.lower() for label in labels_to_check))]
sorted_filtered_df_items = filtered_df_items.sort_values(by='Description').reset_index(drop=True)
# print(sorted_filtered_df_items)

# Convert the "Price String" column to a float with two decimal points
sorted_filtered_df_items['Price'] = sorted_filtered_df_items['Price String'].str.replace(',', '.').str.replace(' €', '').astype(float).round(2)

sorted_filtered_df_items.drop('Price String', axis=1, inplace=True)


def calculate_similarity(args):
    i, desc, description_column, threshold = args
    similar_pairs = []
    for j in range(i + 1, len(description_column)):
        if levenshtein_ratio(desc, description_column[j]) >= threshold:
            similar_pairs.append((i, j))
    return similar_pairs

def find_and_remove_similar(df, threshold=0.9):
    description_column = df['Description'].tolist()
    indices_to_drop = set()
    price_dict = {i: [df.at[i, 'Price']] for i in range(len(df))}

    # Create a pool of processes
    with Pool(processes=cpu_count()) as pool:
        # Execute the tasks in parallel
        results = pool.map(calculate_similarity, [(i, desc, description_column, threshold) for i, desc in enumerate(description_column)])

        # Collect the results
        for result in results:
            for i, j in result:
                if j not in indices_to_drop:
                    price_dict[i].append(df.at[j, 'Price'])
                    indices_to_drop.add(j)

    # Create the new column with lists of prices
    df['All Prices'] = [price_dict[i] for i in range(len(df))]

    # Drop duplicates
    df = df.drop(list(indices_to_drop)).reset_index(drop=True)

    return df
    
    # df.loc[df['Description'].str.contains('apivita', case =False)]['Description'].to_csv('test.csv', index=False)
    
print(sorted_filtered_df_items)

if __name__ == '__main__':
    freeze_support()  # Needed for Windows when creating frozen executables
    # Find and remove similar entries
    find_and_remove_similar(sorted_filtered_df_items)
    # find_and_remove_similar(df_items)
    sorted_filtered_df_items = sorted_filtered_df_items.reset_index(drop=True)
    
    # Create a timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Define the filename
    filename = f'data/filtered_items_{timestamp}.csv'


    # Save DataFrame to CSV
    sorted_filtered_df_items.to_csv(filename, index=False)

    # print(sorted_filtered_df_items.reset_index(drop=True))

# print(sorted_filtered_df_items.shape)