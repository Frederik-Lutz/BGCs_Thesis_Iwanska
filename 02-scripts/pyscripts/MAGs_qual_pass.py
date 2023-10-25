import os
import pandas as pd
import matplotlib.pyplot as plt



path = "/mnt/archgen/users/lutz/bachelorthesis_BGCs_Iwanska/04-analysis/assembly/snakemake/stats/bin_quality"

def extract_statistics_from_data(data):
   
    # Count pass.MIMAG_high
    MIMAG_high = data[data["pass.MIMAG_high"] == True].shape[0]

    # Count pass.MIMAG_medium
    MIMAG_medium = data[data["pass.MIMAG_medium"] == True].shape[0]

    return MIMAG_high, MIMAG_medium

high_pass_counts = []
medium_pass_counts = []
file_names = []

for file in os.listdir(path):
    if file.endswith(".tsv"):
        print(f"----------File: {file}----------")
        data = pd.read_csv(os.path.join(path, file), sep="\t", header=0)
        MIMAG_high, MIMAG_medium = extract_statistics_from_data(data)
        high_pass_counts.append(MIMAG_high)
        medium_pass_counts.append(MIMAG_medium)
        file_names.append(file[:5])

# Sort by sample name
sorted_indices = sorted(range(len(file_names)), key=lambda k: file_names[k])
file_names = [file_names[i] for i in sorted_indices]
high_pass_counts = [high_pass_counts[i] for i in sorted_indices]
medium_pass_counts = [medium_pass_counts[i] for i in sorted_indices]

# Plotting
x = range(len(file_names))
width = 0.35

fig, ax = plt.subplots()
bar1 = ax.bar(x, high_pass_counts, width, label='high')
bar2 = ax.bar([p + width for p in x], medium_pass_counts, width, label='medium')

ax.set_xlabel('sample')
ax.set_ylabel('amount of MAGs')
ax.set_xticks([p + width/2 for p in x])
ax.set_xticklabels(file_names, rotation=45)
ax.legend(title = "quality level")
plt.tight_layout()
plt.show()


total_high_pass = sum(high_pass_counts)
total_medium_pass = sum(medium_pass_counts)

print(f"Total 'high' classifications: {total_high_pass}")
print(f"Total 'medium' classifications: {total_medium_pass}")