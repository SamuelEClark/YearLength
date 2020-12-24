from textblob import TextBlob
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.signal import butter, lfilter
from scipy.signal import freqs
import numpy as np

def butterworth_lowpass(data, cutoff, fs=1, order=4):
    b, a = butter(order, cutoff, btype='low', analog = False, fs=fs)
    y = lfilter(b, a, data)
    return y

df = pd.read_csv("bbcbreaking.csv", delimiter="\t")

def clean_tweet(tweet_string):
    cleaned_whitespace = re.sub(r'\s', " ", tweet_string)
    removed_special_characters = re.sub('[^\w\s]', '', cleaned_whitespace)
    return removed_special_characters

sentiments = []
for each_tweet in df["tweet"]:
    sentiments.append(TextBlob(each_tweet).sentiment[0])

# sns.histplot(sentiments, bins=15)
# plt.show()

sns.lineplot(x=df.time.loc[0:1000], y=sentiments[0:1001])
plt.show()

sns.lineplot(x=df.time.loc[0:1000], y=butterworth_lowpass(sentiments[0:1001], cutoff=4))
plt.show()