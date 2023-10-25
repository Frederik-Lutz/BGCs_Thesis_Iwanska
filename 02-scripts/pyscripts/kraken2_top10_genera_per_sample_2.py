import os
import pandas as pd
import matplotlib.pyplot as plt

# Define column names
columns = ['percentage', 'clade_fragments', 'taxon_fragments', 'rank', 'tax_id', 'scientific_name']

# Empty DataFrame to store all data
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
                'scientific_name': ' '.join(split_line[5:]),
                'sample': filename[:5]
            })

        df = pd.DataFrame(data)
        # Append the data of the current file to the overall data
        all_data = all_data.append(df, ignore_index=True)

# Filter data to include only rows where the rank is "G" (genus)
all_genera = all_data[all_data['rank'] == 'G']

# Group by 'sample' and 'scientific_name' and sum percentages
grouped_genera = all_genera.groupby(['sample', 'scientific_name']).agg({'percentage': 'sum'}).reset_index()

# Find top ten most abundant genera overall
top_genera_overall = grouped_genera.groupby('scientific_name').agg({'percentage': 'sum'}) \
    .sort_values(by='percentage', ascending=False).head(10)

# Filter the data to keep only the top 10 genera
top_10_genera_names = top_genera_overall.index.tolist()
top_10_genera_data = grouped_genera[grouped_genera['scientific_name'].isin(top_10_genera_names)]

# Normalize percentages per genus across all samples
genus_total_percentage = top_10_genera_data.groupby('scientific_name')['percentage'].sum()
top_10_genera_data['normalized_percentage'] = top_10_genera_data.apply(
    lambda row: row['percentage'] / genus_total_percentage[row['scientific_name']], axis=1)

top_10_genera_data = all_genera_norm.query('scientific_name.isin(@top_10_genera_names)')
ax = top_10_genera.plot(kind='bar', stacked=True, colormap='viridis')

plt.xlabel('sample')
plt.ylabel('relative abundance')

# Get handles and labels for the legend
handles, labels = ax.get_legend_handles_labels()

# Adjust the legend to prevent overlap with bars
legend = plt.legend(handles, labels, bbox_to_anchor=(1, 1), loc='upper left')
legend.set_title('genus')

# Make the legend labels italic
for label in legend.get_texts():
    label.set_fontstyle('italic')

plt.show()
