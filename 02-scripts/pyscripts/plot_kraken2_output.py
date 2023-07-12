import os
import pandas as pd
import matplotlib.pyplot as plt

# Define column names
columns = ['percentage', 'clade_fragments', 'taxon_fragments', 'rank', 'tax_id', 'scientific_name']

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

        # Separate genera
        genera_df = df[df['rank'] == 'G']

        # Top ten most abundant genera
        top_genera = genera_df.sort_values(by='percentage', ascending=False).head(10)

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.bar(top_genera['scientific_name'], top_genera['percentage'])
        plt.xlabel("Genus")
        plt.ylabel("Percentage")
        plt.xticks(rotation=90)
        # Save the plot as a PNG file
        plt.savefig(f'/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/05-results/{filename}.png', bbox_inches='tight')    


