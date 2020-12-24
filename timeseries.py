import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

from helpers.filters import butterworth_lowpass

df = pd.read_csv("bbcbreaking.csv", delimiter="\t")

df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
df = df[["date","likes_count", "retweets_count", "replies_count"]].resample('1D', on="date").sum()
print(df.head())

df["likes_cumulative"] = df["likes_count"].cumsum()


sns.lineplot(x = df.index, y=df["likes_cumulative"])
plt.show()

sns.lineplot(x = df.index, y=df["likes_count"])
plt.show()

sns.lineplot(x = df.index, y=butterworth_lowpass(df.likes_count, cutoff=0.01))
plt.show()