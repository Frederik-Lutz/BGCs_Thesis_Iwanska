##################################
#This script is used to generate a plot of the read length distribution
#as a result of nf-core/eager
#15/08/2023
###################################


import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

read_lengths = [148, 148, 147, 149, 147, 148, 145, 145, 146, 145, 145, 145, 144, 144, 145, 145 ]
read_length_median = sum(read_lengths)/len(read_lengths)

plt.figure(figsize=(10, 6))

plt.hist(read_lengths, bins = 20,  weights=np.ones(len(read_lengths)) / len(read_lengths), color='blue', alpha=0.7)
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

plt.text(148, 0.3, f'Mean Read Length across samples: {int(read_length_median)}',fontsize=12, color='red', ha='right')
plt.xlabel('Average Read Length [bp]')
plt.ylabel('Frequency')
plt.title('Read Length Distribution')

plt.show()
