import snscrape.modules.twitter as sntwitter
import pandas as pd
import schedule
import time
import os

# Constants
ACCOUNT_NAME = 'MoonshotListing'
TWEET_COUNT = 1  # Number of recent tweets to fetch
LAST_TWEET_FILE = 'last_tweet_id.txt'

def get_latest_tweet(account_name, tweet_count=1):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterUserScraper(account_name).get_items()):
        if i >= tweet_count:
            break
        tweets.append(tweet)
    return tweets[0] if tweets else None

def read_last_tweet_id():
    if os.path.exists(LAST_TWEET_FILE):
        with open(LAST_TWEET_FILE, 'r') as file:
            return file.read().strip()
    return None

def write_last_tweet_id(tweet_id):
    with open(LAST_TWEET_FILE, 'w') as file:
        file.write(tweet_id)

def notify_new_tweet(tweet):
    # Placeholder for notification logic
    # For example, print to console or send an email
    print(f"New tweet from @{ACCOUNT_NAME}: {tweet.content}")

def check_for_new_tweets():
    latest_tweet = get_latest_tweet(ACCOUNT_NAME, TWEET_COUNT)
    if not latest_tweet:
        print("No tweets found.")
        return

    last_tweet_id = read_last_tweet_id()
    if last_tweet_id != str(latest_tweet.id):
        notify_new_tweet(latest_tweet)
        write_last_tweet_id(str(latest_tweet.id))
    else:
        print("No new tweets.")

# Schedule the check to run every 5 minutes
schedule.every(5).minutes.do(check_for_new_tweets)

print(f"Monitoring @{ACCOUNT_NAME} for new tweets...")

while True:
    schedule.run_pending()
    time.sleep(1)
