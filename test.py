from scipy.stats import ttest_1samp
import numpy as np 
ages = [32,34,29,29,22,39,38,37,38,36,30,26,22,22]

ages_mean = np.mean(ages)

tset, pval = ttest_1samp(ages,27)
print(pval)