# import matplotlib.pyplot as plt
# import pandas as pd

# # Load the data
# data = pd.read_csv("/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash/antiSMASH_combined.tsv", sep='\t')
# df = pd.DataFrame(data)

# # Group by Sample_ID and Product_class and count occurrences
# product_class_counts = df.groupby(['Sample_ID', 'Product_class']).size().unstack(fill_value=0)

# # Group specified Sample_IDs and sum their counts
# selected_samples = ['LS-63', 'LS-65', 'LS', 'LS-85']
# selected_counts = product_class_counts.loc[selected_samples].sum()

# # Sum the counts for the rest of the samples
# rest_counts = product_class_counts.drop(selected_samples, errors='ignore').sum()

# # Plot the abundance for the selected and rest of the samples
# plt.figure(figsize=(12, 6))
# x = range(len(selected_counts))  # the label locations

# # Width of the bars
# bar_width = 0.35

# plt.bar(x, selected_counts, width=bar_width, label='Selected Samples')
# plt.bar([p + bar_width for p in x], rest_counts, width=bar_width, label='Rest of Samples')

# plt.xlabel('Product Class')
# plt.ylabel('Count')
# plt.title('Product Class Counts for Selected Samples vs Rest of Samples')
# plt.xticks([p + bar_width/2 for p in x], selected_counts.index, rotation=45)
# plt.legend()
# plt.tight_layout()
# plt.show()

import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data = pd.read_csv("/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash/antiSMASH_combined.tsv", sep='\t')
df = pd.DataFrame(data)

# Group by Sample_ID and Product_class and count occurrences
product_class_counts = df.groupby(['Sample_ID', 'Product_class']).size().unstack(fill_value=0)

# Group specified Sample_IDs and sum their counts
selected_samples = ['LS-63', 'LS-65', 'LS', 'LS-85']
selected_counts = product_class_counts.loc[selected_samples].sum()

# Sum the counts for the rest of the samples
rest_counts = product_class_counts.drop(selected_samples, errors='ignore').sum()

# Select the top 10 most abundant product classes for each group
top_10_selected = selected_counts.nlargest(10)
top_10_rest = rest_counts.nlargest(10)

# Plot the top 10 most abundant product classes for each group
x = range(len(top_10_selected))  # the label locations
bar_width = 0.35  # Width of the bars

plt.figure(figsize=(12, 6))
plt.bar(x, top_10_selected, width=bar_width, label='hemp retting samples')
plt.bar([p + bar_width for p in x], top_10_rest, width=bar_width, label='non-hemp retting samples')

plt.xlabel('Product Class')
plt.ylabel('Count')

plt.xticks([p + bar_width/2 for p in x], top_10_selected.index, rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

