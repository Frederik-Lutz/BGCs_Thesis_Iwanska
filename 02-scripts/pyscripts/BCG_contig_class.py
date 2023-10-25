import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/05-results/ANNO_BGC_contig_taxclassification.tsv", sep='\t')
df = pd.DataFrame(data)

taxa = df['lineage'].str.extract(r'f_([^;]+)')
taxa = taxa.iloc[:,0].value_counts()
taxa.rename('abundance', inplace=True)
taxa = pd.DataFrame(taxa)

fig, ax = plt.subplots()

ax.barh(taxa.index[0:20], taxa.iloc[0:20,0], color='lightgrey', zorder=3)
ax.set_xlabel("amount of classified contigs")
ax.spines[['top','right']].set_visible(False)
ax.set_title('b',loc='left', fontweight="bold")

plt.rcParams['figure.dpi']=300
plt.tight_layout()
plt.show()