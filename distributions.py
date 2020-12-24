import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

from helpers.filters import butterworth_lowpass

df = pd.read_csv("bbcbreaking.csv", delimiter="\t")

df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
df = df[["date","likes_count", "retweets_count", "replies_count"]].resample('1D', on="date").sum()

sns.histplot(df["likes_count"], binrange=(0,25000))
plt.show()

#TODO: fit to exponential tail

sns.scatterplot(x=df["likes_count"], y=df["retweets_count"])
plt.show()

#TODO: kde (see if clustering will be useful)