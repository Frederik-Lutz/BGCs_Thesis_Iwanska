import os
import pandas as pd
import matplotlib.pyplot as plt

# Define column names
columns = ['percentage', 'clade_fragments', 'taxon_fragments', 'rank', 'tax_id', 'scientific_name']

# Path to the folder containing the text files
folder_path = "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/kraken2"

# Calculate the total percentage sum for all genera
total_percentage_sum = grouped_genera['percentage'].sum()

# Normalize the percentages
top_genera_overall['normalized_percentage'] = top_genera_overall['percentage'] / total_percentage_sum

# Create a DataFrame to store the data for the top genera in each sample
top_genera_samples = pd.DataFrame()

# Iterate over the folder and read all text files
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        filename = filename[:5]

        # Read the data file
        with open(file_path) as f:
            lines = f.read().splitlines()

        data = []
        for line in lines:
            split_line = line.split()
            scientific_name = ' '.join(split_line[5:])
            if split_line[3] == 'G' and scientific_name in top_genera_overall.index:
                data.append({
                    'sample': filename,
                    'scientific_name': scientific_name,
                    'percentage': float(split_line[0])
                })

        df = pd.DataFrame(data)
        top_genera_samples = top_genera_samples.append(df, ignore_index=True)


# Define a function to format the column as italic
def format_italic(cell):
    return 'font-style: italic'

# Apply the formatting function to the desired column
styled_df = df.style.applymap(format_italic, subset=['scientific_name'])


# Pivot the data to create a DataFrame suitable for plotting
pivot_data = top_genera_samples.pivot(index='sample', columns='scientific_name', values='percentage')

# Plot the data
plt.figure(figsize=(12, 6))

ax = pivot_data.plot(kind='bar', stacked=True, colormap='viridis')

plt.xlabel('sample')
plt.ylabel('frequency')

# Get handles and labels for the legend
handles, labels = ax.get_legend_handles_labels()

# Modify the labels to be italic using LaTeX formatting
italic_labels = [f"$\it{{{label}}}$" for label in labels]

# Adjust the legend to prevent overlap with bars
plt.legend(handles, italic_labels, title='genus', bbox_to_anchor=(1, 1), loc='upper left')

plt.show()
