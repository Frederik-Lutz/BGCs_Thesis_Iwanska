# This directory contains the scripts used in the bachelorthesis_BGCs_Iwanska project
# Downloading data

- `AncientMetagenomeDir_aspera_download_script.sh`
   was used to download ra sequencing data by running
   ```
  ASPERA_PATH=/usr/local64/opt/aspera/connect bash AncientMetagenomeDir_aspera_download_script.sh
  ```
   
- `md5sum_script.sh` was used to create hash codes for downloaded files and was compared to the hash codes on ENA using `pyscripts/comp_md5.py`

### nf-core/eager

To combine forward- and reverse reads as well processing the raw data, the pipeline was run as follows:
```
nextflow run nf-core/eager -r 2.4.6 \
        -profile eva,archgen \
        --input "01-documentation/AncientMetagenomeDir_nf_core_eager_input_table.tsv" \
        --fasta '/mnt/archgen/Reference_Genomes/Human/hs37d5/hs37d5.fa' \
        --fasta_index '/mnt/archgen/Reference_Genomes/Human/hs37d5/hs37d5.fa.fai' \
        --bwa_index '/mnt/archgen/Reference_Genomes/Human/hs37d5' \
        --seq_dict '/mnt/archgen/Reference_Genomes/Human/hs37d5/hs37d5.dict' \
        --skip_preseq \
        --skip_deduplication \
        --skip_qualimap \
        --skip_collapse \
        --bwaalno 1 --bwaalnl 32 \
        --outdir "04-analysis/eager"
  ```
