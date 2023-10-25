import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv(
    "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/antismash/antiSMASH_combined.tsv", sep='\t')
df = pd.DataFrame(data)

complete_contigs = df.iloc[:, [0, 2, 3, 5, 8]]
complete_contigs = complete_contigs[complete_contigs['BGC_complete'] == 'Yes']

data = pd.read_csv(
    '/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/05-results/QUAL_pyDamage_results_BGCcontigs.tsv', sep='\t')
df = pd.DataFrame(data)

ancient_contigs = df.iloc[:, [0,1,2,12]]
ancient_contigs = ancient_contigs[(ancient_contigs['predicted_accuracy']>= 0.5) & (ancient_contigs['qvalue']<= 0.05)]
ancient_contigs['Contig_ID'] = ancient_contigs['reference']

merged_df = complete_contigs.merge(ancient_contigs, on='Contig_ID', how='inner')
print(merged_df['Sample_ID'].value_counts())