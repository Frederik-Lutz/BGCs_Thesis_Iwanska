import matplotlib.pyplot as plt
import pandas as pd

# Load the data and add info about hemp-retting
data = pd.read_csv("/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash/antiSMASH_combined.tsv", sep='\t')
df = pd.DataFrame(data)
df['hemp_retting'] = "no"
df.loc[df['Sample_ID'].isin(['LS-63', 'LS-65', 'LS', 'LS-85']), 'hemp_retting'] = "yes"

# Group by hemp retting and Product_class and count occurrences
product_class_counts = df.groupby(['Product_class', 'hemp_retting']).size().unstack(fill_value=0)
product_class_complete_counts = df.query('BGC_complete == "Yes"') \
    .groupby(['Product_class', 'hemp_retting']).size().unstack(fill_value=0)

# Convert into relative abundances by hemp retting
product_class_relab = product_class_counts / product_class_counts.sum(axis=0) * 100
product_class_complete_relab = product_class_complete_counts / product_class_complete_counts.sum(axis=0) *100

# Select the top 10 most abundant product classes for each group
top10_products = product_class_relab.max(axis=1).nlargest(10)
top10_complete_products = product_class_complete_relab.max(axis=1).nlargest(10)

# Subset data
product_class_relab_top10 = product_class_relab.loc[product_class_relab.index.isin(top10_products.index.tolist())]
product_class_complete_relab_top10 = product_class_complete_relab.loc[product_class_complete_relab.index.isin(top10_complete_products.index.tolist())]


# Plot the relative abundance for the top 10 most abundant product classes
x = range(10)  # the label locations
bar_width = 0.35  # Width of the bars

# Create subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 12))

# Plot for all BGCs
axs[0].bar(x, product_class_relab_top10.loc[top10_products.index]['yes'],
           width=bar_width, label='hemp retting samples')
axs[0].bar([p + bar_width for p in x], product_class_relab_top10.loc[top10_products.index]['no'],
           width=bar_width, label='non-hemp retting samples')

axs[0].set_xlabel('product class')
axs[0].set_ylabel('relative abundance [%]')
axs[0].set_xticks([p + bar_width/2 for p in x])
axs[0].set_xticklabels(top10_products.index, rotation=45)
axs[0].legend()
axs[0].set_title('a', loc='left', fontweight="bold")

# Plot for complete BGCs
axs[1].bar(x, product_class_complete_relab_top10.loc[top10_complete_products.index]['yes'],
           width=bar_width, label='hemp retting samples')
axs[1].bar([p + bar_width for p in x], product_class_complete_relab_top10.loc[top10_complete_products.index]['no'],
           width=bar_width, label='non-hemp retting samples')

axs[1].set_xlabel('product class')
axs[1].set_ylabel('relative abundance [%]')
axs[1].set_xticks([p + bar_width/2 for p in x])
axs[1].set_xticklabels(top10_complete_products.index, rotation=45)
axs[1].legend()
axs[1].set_title('b', loc='left', fontweight="bold")


plt.tight_layout()
plt.show()
