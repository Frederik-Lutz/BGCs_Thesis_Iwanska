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

        df = pd.DataFrame(data).assign(sample=os.path.basename(file_path).replace(".txt", ""))
        # Append the data of the current file to the overall data
        all_data = all_data.append(df, ignore_index=True)

# Filter out genera
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

# Calculate the total percentage sum for all genera
#total_percentage_sum = grouped_genera['percentage'].sum()

# Normalize the percentages
#top_genera_overall['normalized_percentage'] = top_genera_overall['percentage'] / total_percentage_sum

# Plot the data
plt.figure(figsize=(12, 6))

# Plot the horizontal bar chart with normalized percentages
bars = plt.barh(top_genera_overall.index, top_genera_overall['percentage'])

# Modify the y-axis labels to be italic using LaTeX formatting
italic_labels = [f"$\it{{{label}}}$" for label in top_genera_overall.index]
plt.yticks(range(len(top_genera_overall.index)), italic_labels)  # Set custom tick positions and labels

plt.xlabel('normalized relative abundance')
plt.ylabel('genus')

# Set y-axis limits
plt.ylim(-0.5, len(top_genera_overall) - 0.5)

# Add data labels to the bars
#for bar in bars:
#    plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
#             f'{bar.get_width()*100:.2f}%', 
#             va='center', ha='left', fontsize=10, color='black')

plt.gca().invert_yaxis()  # Invert y-axis to have the highest value at the top
plt.show()
