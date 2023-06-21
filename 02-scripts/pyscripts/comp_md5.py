from glob import glob
import os
import pandas as pd


# Read ENA table directly from URL
ena_report = pd.read_csv("/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/03-data/raw_data/ENA_report.tsv", sep="\t")

# Select samples of interest
ena_report = ena_report.query('run_accession.isin(["ERR4334727","ERR4334729","ERR4334730","ERR4334728","ERR4334731","ERR4334732","ERR4334733", \
                                                "ERR4334734","ERR4334735","ERR4334736","ERR3804375","ERR3804374","ERR3804378","ERR3804373","ERR3804376","ERR3804377"])') \
    .set_index(['run_accession'])

def compare_md5sum(sample, read, tbl):

    # Read calculated md5sum from file
    with open(f"{sample}_{read}.fastq.gz.md5", "rt") as md5file:
        calc_md5 = md5file.readline().split()[0]
    
    # Extract expected md5sum from table
    exp_md5 = tbl.at[sample, 'fastq_md5'].split(";")[read - 1]
    
    # Compare the hashes
    if calc_md5 == exp_md5:
        print(f"Correct md5sum hash for {sample}_{read}.fastq.gz")
    else:
       print(f"Incorrect md5sum hash for {sample}_{read}.fastq.gz")

for sample in ena_report.index.values:
    for read in [1, 2]:
        compare_md5sum(sample, read, ena_report)
