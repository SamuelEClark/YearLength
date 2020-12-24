import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.signal import butter, lfilter
from scipy.signal import freqs
import numpy as np

df = pd.read_csv("bbcbreaking.csv", delimiter="\t")

df["likes_cumulative"] = df["likes_count"].cumsum()

sns.lineplot(x = df.time[0:1000], y = df.likes_cumulative[0:1000])
plt.show()