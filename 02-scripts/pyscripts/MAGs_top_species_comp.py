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

# List of regex patterns to try
regex_patterns = [r's__([^;]+)', r'g__([^;]+)', r'f__([^;]+)', r'o__([^;]+)']

# Lists to store extracted strings based on conditions for the first file
phylum_bac_s = []
phylum_bac_g = []
phylum_bac_f = []
phylum_bac_o = []

# Lists to store extracted strings for second file
phylum_ar_s = []
phylum_ar_g = []
phylum_ar_f = []
phylum_ar_o = []

# Iterate through each object in 'classification' for the first file
for classification in gtdbtk_bac['classification']:
    # Iterate through each regex pattern in order
    for pattern in regex_patterns:
        match = re.search(pattern, str(classification))  # Convert to string for regex
        if match:
            # Append the extracted phylum information based on the pattern
            if pattern.startswith('s__'):
                phylum_bac_s.append(match.group(1))
            elif pattern.startswith('g__'):
                phylum_bac_g.append(match.group(1))
            elif pattern.startswith('f__'):
                phylum_bac_f.append(match.group(1))
            elif pattern.startswith('o__'):
                phylum_bac_o.append(match.group(1))
            break  # Move to the next classification

# Iterate through each object in 'classification' for the second file
for classification in gtdbtk_ar['classification']:
    # Iterate through each regex pattern in order
    for pattern in regex_patterns:
        match = re.search(pattern, str(classification))  # Convert to string for regex
        if match:
            # Append the extracted phylum information based on the pattern
            if pattern.startswith('s__'):
                phylum_ar_s.append(match.group(1))
            elif pattern.startswith('g__'):
                phylum_ar_g.append(match.group(1))
            elif pattern.startswith('f__'):
                phylum_ar_f.append(match.group(1))
            elif pattern.startswith('o__'):
                phylum_ar_o.append(match.group(1))
            break  # Move to the next classification

# Print the extracted phylum information
print("Phylum based on pattern 's__' for gtdbtk_bac:", phylum_bac_s)
print("Phylum based on pattern 'g__' for gtdbtk_bac:", phylum_bac_g)
print("Phylum based on pattern 'f__' for gtdbtk_bac:", phylum_bac_f)
print("Phylum based on pattern 'o__' for gtdbtk_bac:", phylum_bac_o)

print(len(phylum_bac_s))
print(len(phylum_bac_g))
print(len(phylum_bac_f))
print(len(phylum_bac_o))

print("Phylum based on pattern 's__' for gtdbtk_ar:", phylum_ar_s)
print("Phylum based on pattern 'g__' for gtdbtk_ar:", phylum_ar_g)
print("Phylum based on pattern 'f__' for gtdbtk_ar:", phylum_ar_f)
print("Phylum based on pattern 'o__' for gtdbtk_ar:", phylum_ar_o)

print(len(phylum_ar_s))
print(len(phylum_ar_g))
print(len(phylum_ar_f))
print(len(phylum_ar_o))

# Plotting the lengths of classifications for each list
categories = ['species', 'genus', 'family', 'order']
bac_lengths = [len(phylum_bac_s), len(phylum_bac_g), len(phylum_bac_f), len(phylum_bac_o)]
ar_lengths = [len(phylum_ar_s), len(phylum_ar_g), len(phylum_ar_f), len(phylum_ar_o)]

plt.figure(figsize=(10, 6))
bar_width = 0.35

plt.bar(np.arange(len(categories)), bac_lengths, bar_width, label='gtdbtk_bac')
plt.bar(np.arange(len(categories)) + bar_width, ar_lengths, bar_width, label='gtdbtk_ar')

plt.xlabel('Taxonomic Level')
plt.ylabel('Number of Classifications')
plt.title('Length of Classifications for Each Taxonomic Level')
plt.xticks(np.arange(len(categories)) + bar_width / 2, categories)
plt.legend()
plt.tight_layout()
plt.show()
