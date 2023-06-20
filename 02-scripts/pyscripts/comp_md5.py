from glob import glob
import os
import pandas as pd

def compare_md5sum(sample, read, tbl):
    # Read calculated md5sum from file
    with open(f"download_files/{sample}_{read}.md5", "rt") as md5file:
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
