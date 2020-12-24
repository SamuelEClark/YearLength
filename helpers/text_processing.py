import re

def clean_tweet(tweet_string):
    cleaned_whitespace = re.sub(r'\s', " ", tweet_string)
    removed_special_characters = re.sub('[^\w\s]', '', cleaned_whitespace)
    return removed_special_characters
