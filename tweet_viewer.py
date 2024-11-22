import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st

# Function to scrape tweets
def get_latest_tweets(account_name, tweet_count=10):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterUserScraper(account_name).get_items()):
        if i >= tweet_count:
            break
        tweets.append([tweet.date, tweet.content])
    return pd.DataFrame(tweets, columns=["Date", "Tweet"])

# Streamlit UI
st.title("Twitter Account Scraper")
st.write("Fetch recent tweets from any public Twitter account.")

# Input Fields
account_name = st.text_input("Enter Twitter Username (without @):", "elonmusk")
tweet_count = st.slider("Number of Tweets to Fetch", min_value=1, max_value=100, value=10)

# Fetch Tweets
if st.button("Fetch Tweets"):
    with st.spinner("Fetching tweets..."):
        try:
            tweets_df = get_latest_tweets(account_name, tweet_count)
            st.success(f"Fetched {len(tweets_df)} tweets from @{account_name}.")
            st.dataframe(tweets_df)  # Display as interactive table
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Optional: Download Tweets as CSV
if 'tweets_df' in locals():
    csv = tweets_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Tweets as CSV",
        data=csv,
        file_name=f"{account_name}_tweets.csv",
        mime="text/csv"
    )