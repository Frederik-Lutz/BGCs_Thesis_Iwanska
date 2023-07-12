import os
import pandas as pd
import matplotlib.pyplot as plt

# Define column names
columns = ['percentage', 'clade_fragments', 'taxon_fragments', 'rank', 'tax_id', 'scientific_name']

#empty DataFrame to store all data
all_data = pd.DataFrame()

# Path to the folder containing the text files
folder_path = "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/kraken2"

# Iterate over the folder and read all text files
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        # Read the data file
        with open(file_path) as f:
            lines = f.read().splitlines()

        data = []
        for line in lines:
            split_line = line.split()
            data.append({
                'percentage': float(split_line[0]),
                'clade_fragments': int(split_line[1]),
                'taxon_fragments': int(split_line[2]),
                'rank': split_line[3],
                'tax_id': int(split_line[4]),
                'scientific_name': ' '.join(split_line[5:])
            })

        df = pd.DataFrame(data)
        # Append the data of the current file to the overall data
        all_data = all_data.append(df, ignore_index=True)

# Filter out genera
all_genera = all_data[all_data['rank'] == 'G']

# Group by 'scientific_name' and sum percentages
grouped_genera = all_genera.groupby('scientific_name').agg({'percentage': 'sum'})

# Find top ten most abundant genera overall
top_genera_overall = grouped_genera.sort_values(by='percentage', ascending=False).head(10)

# Plot the data
plt.figure(figsize=(12, 6))
plt.barh(top_genera_overall.index, top_genera_overall['percentage'])
plt.xlabel('Total Percentage')
plt.ylabel('Genus')
plt.title('Top 10 Genera Overall')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest value at the top
plt.show()