import pandas as pd
import matplotlib.pyplot as plt

hemp_retters = ["LS-63", "LS-65", "LS-67", "LS-85"]
non_hemp_retters = ["LS-35", "LS-55", "LS-76", "LS-93"]

retters_paths = [
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-63-megahit/metawrap_50_10_bins.contigs",
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-65-megahit/metawrap_50_10_bins.contigs",
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-67-megahit/metawrap_50_10_bins.contigs",
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-85-megahit/metawrap_50_10_bins.contigs"
]

non_retters_paths = [
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-35-megahit/metawrap_50_10_bins.contigs",
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-55-megahit/metawrap_50_10_bins.contigs",
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-76-megahit/metawrap_50_10_bins.contigs",
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/binning/metawrap/BIN_REFINEMENT/LS-93-megahit/metawrap_50_10_bins.contigs"
]

data_ = pd.read_csv(
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash/antiSMASH_combined.tsv", sep='\t')

sample_ids = data_["Sample_ID"]
contig_ids = data_["Contig_ID"]

# Create dataframes to store the binned counts for retters and non-retters
binned_contigs_retters = pd.DataFrame({'Sample': hemp_retters, 'binned': [0] * len(hemp_retters)})
binned_contigs_non_retters = pd.DataFrame({'Sample': non_hemp_retters, 'binned': [0] * len(non_hemp_retters)})

for i, file_path in enumerate(retters_paths):
    data = pd.read_csv(file_path, delimiter="\t", header=None, names=['contig', 'bin'])
    contigs = set(data['contig'].tolist())
    number = len(contigs)  # Count the unique contigs
    binned_contigs_retters.at[i, 'binned'] = number

for i, file_path in enumerate(non_retters_paths):
    data = pd.read_csv(file_path, delimiter="\t", header=None, names=['contig', 'bin'])
    contigs = set(data['contig'].tolist())
    number = len(contigs)  # Count the unique contigs
    binned_contigs_non_retters.at[i, 'binned'] = number

print("Binned contigs for hemp retters:")
print(binned_contigs_retters)

print("\nBinned contigs for non-hemp retters:")
print(binned_contigs_non_retters)

# Function to find overlapping contigs with contig_ids
def find_overlapping_contigs(sample_contigs, all_contigs):
    overlapping_contigs = set(sample_contigs) & set(all_contigs)
    return list(overlapping_contigs)

# Find overlapping contigs for hemp retters
overlapping_contigs_hemp_retters = []
for i, file_path in enumerate(retters_paths):
    data = pd.read_csv(file_path, delimiter="\t", header=None, names=['contig', 'bin'])
    contigs = data['contig'].tolist()
    overlapping_contigs = find_overlapping_contigs(contigs, contig_ids)
    sample_id = hemp_retters[i]
    overlapping_contigs_hemp_retters.append({'Sample': sample_id, 'Overlapping_Contigs': overlapping_contigs, 'Length': len(overlapping_contigs)})

# Find overlapping contigs for non-hemp retters
overlapping_contigs_non_hemp_retters = []
for i, file_path in enumerate(non_retters_paths):
    data = pd.read_csv(file_path, delimiter="\t", header=None, names=['contig', 'bin'])
    contigs = data['contig'].tolist()
    overlapping_contigs = find_overlapping_contigs(contigs, contig_ids)
    sample_id = non_hemp_retters[i]
    overlapping_contigs_non_hemp_retters.append({'Sample': sample_id, 'Overlapping_Contigs': overlapping_contigs, 'Length': len(overlapping_contigs)})

# # Print the results
# print("Overlapping contigs for hemp retters:")
# for item in overlapping_contigs_hemp_retters:
#     print(item)

# print("\nOverlapping contigs for non-hemp retters:")
# for item in overlapping_contigs_non_hemp_retters:
#     print(item)


# Function to count overlapping contigs with contig_ids
def count_overlapping_contigs(sample_contigs, all_contigs):
    overlapping_contigs = set(sample_contigs) & set(all_contigs)
    return len(overlapping_contigs)

# Count overlapping contigs for hemp retters
overlap_counts_hemp_retters = []
for i, file_path in enumerate(retters_paths):
    data = pd.read_csv(file_path, delimiter="\t", header=None, names=['contig', 'bin'])
    contigs = data['contig'].tolist()
    overlap_count = count_overlapping_contigs(contigs, contig_ids)
    sample_id = hemp_retters[i]
    overlap_counts_hemp_retters.append({'Sample': sample_id, 'Overlap_Count': overlap_count})

# Count overlapping contigs for non-hemp retters
overlap_counts_non_hemp_retters = []
for i, file_path in enumerate(non_retters_paths):
    data = pd.read_csv(file_path, delimiter="\t", header=None, names=['contig', 'bin'])
    contigs = data['contig'].tolist()
    overlap_count = count_overlapping_contigs(contigs, contig_ids)
    sample_id = non_hemp_retters[i]
    overlap_counts_non_hemp_retters.append({'Sample': sample_id, 'Overlap_Count': overlap_count})

# Print the counts
print("Overlap counts for hemp retters:")
for item in overlap_counts_hemp_retters:
    print(item)

print("\nOverlap counts for non-hemp retters:")
for item in overlap_counts_non_hemp_retters:
    print(item)

# Data preparation
hemp_retter_samples = [item['Sample'] for item in overlap_counts_hemp_retters]
hemp_retter_counts = [item['Overlap_Count'] for item in overlap_counts_hemp_retters]

non_hemp_retter_samples = [item['Sample'] for item in overlap_counts_non_hemp_retters]
non_hemp_retter_counts = [item['Overlap_Count'] for item in overlap_counts_non_hemp_retters]

# Calculate the sum of counts for all retters
all_counts = sum(item['Overlap_Count'] for item in overlap_counts_hemp_retters) + sum(item['Overlap_Count'] for item in overlap_counts_non_hemp_retters)

# Calculate relative abundances
rel_ab_retters = [(count / all_counts) * 100 for count in hemp_retter_counts]
rel_ab_non_retters = [(count / all_counts) * 100 for count in non_hemp_retter_counts]

# Plotting
plt.figure(figsize=(10, 6))

# Bar plot for hemp retters
plt.bar(hemp_retter_samples, rel_ab_retters, label='Relative Abundance Hemp Retters')

# Bar plot for non-hemp retters
plt.bar(non_hemp_retter_samples, rel_ab_non_retters, label='Relative Abundance Non-Hemp Retters')

plt.xlabel('sample')
plt.ylabel('relative abundance (%)')
#plt.title('Relative Abundance of Binned BGCs for Hemp and Non-Hemp Retters')
plt.legend()
plt.tight_layout()
plt.xticks(rotation=45)
plt.show()
