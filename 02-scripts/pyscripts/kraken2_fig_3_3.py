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
                'sample_name' : filename[:5]  # Use the first 5 characters of the filename
            })

        df = pd.DataFrame(data).assign(sample=os.path.basename(file_path).replace(".txt", ""))
        # Append the data of the current file to the overall data
        all_data = all_data.append(df, ignore_index=True)

# Filter data for genus-level taxa
all_genera = all_data[all_data['rank'] == 'G']

# Normalized per sample
all_genera_total = all_genera.groupby(['sample']).agg({'clade_fragments': 'sum'}) \
    .rename({'clade_fragments': 'total'}, axis=1).reset_index()
all_genera_norm = all_genera[['sample', 'scientific_name', 'clade_fragments']] \
    .merge(all_genera_total, how="left", on="sample") \
    .assign(percentage = lambda x: x.clade_fragments / x.total * 100)

# Group by 'scientific_name' and sum percentages
grouped_genera = all_genera_norm.groupby('scientific_name').agg({'percentage': 'sum'})

# Find top ten most abundant genera overall
top_genera_overall = grouped_genera.sort_values(by='percentage', ascending=False).head(10)

# Get the names of the top 10 genera
top_genera_names = top_genera_overall.index.tolist()

# Find top ten most abundant genera overall
top_genera_overall = grouped_genera.sort_values(by='percentage', ascending=False).head(10)

# Get the names of the top 10 genera
top_10_genera_names = top_genera_overall.index.tolist()

# Filter the data to keep only the top 10 genera
top_10_genera_data = all_genera_norm[all_genera_norm['scientific_name'].isin(top_10_genera_names)]

plt.figure(figsize=(12, 6))

# Pivot the data for plotting
pivot_data = top_10_genera_data.pivot_table(index='sample', columns='scientific_name', values='percentage', fill_value=0)

# Plot stacked bar plot
ax = pivot_data.plot(kind='bar', stacked=True, colormap='viridis', figsize=(12, 8))

plt.xlabel('sample')
plt.ylabel('relative abundance')

# Set legend properties to make font italic
legend = ax.legend(title='Genus', bbox_to_anchor=(1, 1), loc='upper left')
legend.set_title('genus')
for label in legend.get_texts():
    label.set_fontstyle('italic')

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()