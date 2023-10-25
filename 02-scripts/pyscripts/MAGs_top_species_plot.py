import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load data for the first file
gtdbtk_bac = pd.read_csv(
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/stats/gtdbtk/gtdbtk.lakeSediments_bac120.summary.tsv",
    sep="\t")

gtdbtk_ar = pd.read_csv(
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/stats/gtdbtk/gtdbtk.lakeSediments_ar53.summary.tsv",
    sep="\t")

gtdbtk = pd.concat([gtdbtk_bac, gtdbtk_ar])

# Extract phylum using regex
phylum = gtdbtk['classification'].str.extract(r'f__([^;]+)')

# Calculate the number of MAGs that were not assigned at the family level
rest = gtdbtk['classification'].str.count(r'f__(?=$|;)')

# Count occurrences of each phylum
phylum_counts = phylum.iloc[:, 0].value_counts()
phylum_counts.rename('abundance', inplace=True)
phylum_counts = pd.DataFrame(phylum_counts)

# Get the top 20 phyla or less if there are fewer
top_phyla = phylum_counts.iloc[:20]

# Create a figure and a set of subplots
fig, ax = plt.subplots(figsize=(10, 6))

# Create the horizontal bar plot
ax.barh(top_phyla.index, top_phyla['abundance'], color='lightgrey', zorder=3)
ax.set_xlabel("amount of classified MAGs")
plt.yticks(fontsize=12, fontstyle='italic')

plt.rcParams['figure.dpi'] = 300
plt.tight_layout()
plt.show()

print("Number of MAGs not assigned at the family level:", rest.sum())
