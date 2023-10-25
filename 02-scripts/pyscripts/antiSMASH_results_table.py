import os
import pandas as pd
import matplotlib.pyplot as plt

# # Define the main folder path
# main_folder = '/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash'

# # Get a list of subdirectories that start with "LS-"
# subdirectories = [subdir for subdir in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, subdir)) and subdir.startswith('LS-')]

# # Initialize an empty DataFrame to store the concatenated data
# concatenated_data = pd.DataFrame()

# # Iterate through each subdirectory
# for subdir in subdirectories:
#     subdirectory_path = os.path.join(main_folder, subdir)
    
#     # Get a list of TSV files in the subdirectory
#     tsv_files = [file for file in os.listdir(subdirectory_path) if file.endswith('.tsv')]
    
#     # Concatenate TSV files within the subdirectory
#     for tsv_file in tsv_files:
#         tsv_file_path = os.path.join(subdirectory_path, tsv_file)
#         df = pd.read_csv(tsv_file_path, sep='\t')
#         concatenated_data = pd.concat([concatenated_data, df], ignore_index=True)

# # Print some information about the concatenated data
# print('Concatenated data:')
# print(concatenated_data.head())  # Print the first few rows of the concatenated data

# # Save the concatenated data to a new TSV file
# concatenated_file_path = '/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash/concatenated_file.tsv'
# concatenated_data.to_csv(concatenated_file_path, sep='\t', index=False)
# print(f'Concatenated data saved to {concatenated_file_path}')


# Read the TSV file into a DataFrame
file_path = '/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash/antiSMASH_combined.tsv'  

data = pd.read_csv(file_path, sep='\t')

# Calculate the counts of 'BGC_complete' assignments for each unique 'Sample_ID'
complete_bgc_counts = data.groupby(['Sample_ID', 'BGC_complete']).size().unstack().fillna(0)

# Print the counts for 'BGC_complete' being 'No' and 'Yes' for each unique 'Sample_ID'
print('Counts of BGC_complete assignments for each unique Sample_ID:')
print(complete_bgc_counts)

# Calculate the counts of 'BGC_complete' assignments for each unique 'Sample_ID'
bgc_counts = data.groupby('BGC_complete').size()

# Calculate the sum of complete BGCs and incomplete BGCs
sum_complete_bgc = bgc_counts.get('Yes', 0)
sum_incomplete_bgc = bgc_counts.get('No', 0)

# Calculate the sum of both complete and incomplete BGCs
sum_total_bgc = sum_complete_bgc + sum_incomplete_bgc

# Print the sums
print('Sum of complete BGCs:', sum_complete_bgc)
print('Sum of incomplete BGCs:', sum_incomplete_bgc)
print('Sum of complete and incomplete BGCs:', sum_total_bgc)


# Calculate the counts of each product class
product_class_counts = data['Product_class'].value_counts()

# Select the top 10 most abundant product classes
top_10_product_classes = product_class_counts.head(10)

# # Plot the top 10 most abundant product classes
# plt.figure(figsize=(12, 6))
# top_10_product_classes.plot(kind='bar')
# plt.xlabel('Product Class')
# plt.ylabel('Count')
# plt.tight_layout()
# plt.show()


# Specify the selected samples
selected_samples = ['LS-63', 'LS-65', 'LS', 'LS-85']

# Filter the data for the selected samples and calculate the counts of 'BGC_complete' assignments
selected_data = data[data['Sample_ID'].isin(selected_samples)]
selected_bgc_counts = selected_data.groupby('BGC_complete').size()

# Calculate the sum of complete BGCs and incomplete BGCs for the selected samples
sum_selected_complete_bgc = selected_bgc_counts.get('Yes', 0)
sum_selected_incomplete_bgc = selected_bgc_counts.get('No', 0)



# Print the relative abundance for the selected samples
#print('Relative Abundance of Complete BGCs for Selected Samples:', relative_abundance_selected_complete)
#print('Relative Abundance of Incomplete BGCs for Selected Samples:', relative_abundance_selected_incomplete)

# Calculate the counts of 'BGC_complete' assignments for the rest of the samples
rest_data = data[~data['Sample_ID'].isin(selected_samples)]
rest_bgc_counts = rest_data.groupby('BGC_complete').size()

# Calculate the sum of complete BGCs and incomplete BGCs for the rest of the samples
sum_rest_complete_bgc = rest_bgc_counts.get('Yes', 0)
sum_rest_incomplete_bgc = rest_bgc_counts.get('No', 0)


# Calculate the relative abundance for complete and incomplete BGCs for the selected samples
relative_abundance_selected_complete = sum_selected_complete_bgc / (sum_selected_complete_bgc + sum_rest_complete_bgc)
relative_abundance_selected_incomplete = sum_selected_incomplete_bgc / (sum_rest_incomplete_bgc + sum_selected_incomplete_bgc)

# Calculate the relative abundance for complete and incomplete BGCs for the rest of the samples
relative_abundance_rest_complete = sum_rest_complete_bgc / (sum_rest_complete_bgc + sum_selected_complete_bgc)
relative_abundance_rest_incomplete = sum_rest_incomplete_bgc / (sum_selected_incomplete_bgc + sum_rest_incomplete_bgc)

# Print the relative abundance for the rest of the samples
#print('Relative Abundance of Complete BGCs for Rest of the Samples:', relative_abundance_rest_complete)
#print('Relative Abundance of Incomplete BGCs for Rest of the Samples:', relative_abundance_rest_incomplete)

# Print the results in a tabular format
print("{:<20} {:<15} {:<15} {:<35} {:<35}".format('Sample Group', 'Complete BGCs', 'Incomplete BGCs', 'Relative Abundance of Complete BGCs', 'Relative Abundance of Incomplete BGCs'))
print("{:<20} {:<15} {:<15} {:<35.2%} {:<35.2%}".format('Selected Samples', sum_selected_complete_bgc, sum_selected_incomplete_bgc, relative_abundance_selected_complete, relative_abundance_selected_incomplete))
print("{:<20} {:<15} {:<15} {:<35.2%} {:<35.2%}".format('Rest of the Samples', sum_rest_complete_bgc, sum_rest_incomplete_bgc, relative_abundance_rest_complete, relative_abundance_rest_incomplete))

##################################################
### Pydamage ###
##################################################

# Load the data
data = pd.read_csv('/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/05-results/QUAL_pyDamage_results_BGCcontigs.tsv', sep='\t')
df = pd.DataFrame(data)

# Select the relevant columns
ancient_contigs = df.iloc[:, [0, 1, 2, 11, 12, 18]]

# Filter for ancient contigs
ancient_contigs = ancient_contigs[(ancient_contigs['predicted_accuracy'] >= 0.5) & (ancient_contigs['qvalue'] < 0.05)]

# Count the ancient contigs for each unique sample
ancient_counts_per_sample = ancient_contigs['sample'].value_counts()

# Print the counts
print("Ancient contig counts per unique sample:")
print(ancient_counts_per_sample)

