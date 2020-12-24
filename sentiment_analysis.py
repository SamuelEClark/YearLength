from textblob import TextBlob
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

from helpers.filters import butterworth_lowpass
from helpers.text_processing import clean_tweet

# read data
df = pd.read_csv("bbcbreaking.csv", delimiter="\t", parse_dates=True)

# acquire tweet sentiment
sentiments = []
for each_tweet in df["tweet"]:
    sentiments.append(TextBlob(each_tweet).sentiment[0])
df["sentiments"] = sentiments

# format date column and resample at daily rate (this also makes the timeseries equally spaced, which helps).
# .sum() aggregation, may want to consider averaging the sentiments (median) or similar later.
df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True)
df = df[["date","likes_count", "sentiments", "retweets_count", "replies_count"]].resample('1D', on="date").sum()
print(df.head())

# drop a fat one
plot = sns.lineplot(x=df.index, y=df.sentiments)
sns.lineplot(x=df.index, y=butterworth_lowpass(df.sentiments, cutoff=0.05))
plot.axhline(0, linestyle='dashed', color='0000', alpha=0.4)
plt.show()