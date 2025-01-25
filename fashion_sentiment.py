#Import required liberaries
from transformers import pipeline  # Import pipeline for sentiment analysis
import pandas as pd
import tweepy

import time

# Add a delay to prevent hitting rate limits
time.sleep(15)  # Wait for 15 seconds before the next request


# Twitter API credentials
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEJZwgEAAAAAD4pkPk72wm939DsoCRAUtpuIzDs%3Dh9p7X9icXrc9uZvzeeZKvFPuqjC9E0CWyYSEqu41FbANpM7oi9"  # Add this

# Authenticate using API v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import re

# Twitter API credentials
API_KEY = "tLsjeVWAmTeeJhpFSvUA3qxbY"
API_SECRET = "jEhlUsuf5FIKS5O0DqhwbdylmCLkXX2qodUM1PFtNkUQ9NKiga"
ACCESS_TOKEN = "1649847772835635202-CAyr7G0SAE83nr4cY8ovZXycJZOcSd"
ACCESS_TOKEN_SECRET = "aDykgHgApJiGgbouMEqn21KFW9lTHIb9N1JlnwDDwYD9i"

if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise ValueError("One or more Twitter API credentials are missing!")


# Authenticate with Twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to clean tweets
def clean_tweet(tweet):
    tweet = re.sub(r'@[A-Za-z0-9_]+', '', tweet)  # Remove mentions
    tweet = re.sub(r'https?://\S+', '', tweet)    # Remove URLs
    tweet = re.sub(r'[^a-zA-Z\s]', '', tweet)    # Remove special characters
    return tweet

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
# Function to analyze sentiment
def analyze_sentiment(tweet):
    result = sentiment_pipeline(text)[0]
    return result['label']  # Extract the sentiment label
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

# Replace 'API' with 'Client'
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

# Analyze sentiment (dummy function, replace with your sentiment analysis logic)
from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1:
        return "Positive"
    elif analysis.sentiment.polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"


def fetch_tweets(keyword, count):
    tweet_data = []
    next_token = None  # For pagination
    remaining_count = count

    while remaining_count > 0:
        try:
            # Fetch tweets
            response = client.search_recent_tweets(
                query=keyword,
                tweet_fields=["text", "created_at"],
                max_results=min(remaining_count, 100),  # Fetch up to 100 tweets per call
                next_token=next_token  # Use pagination token
            )

            # Check if there are tweets in the response
            if response.data:
                for tweet in response.data:
                    tweet_data.append({
                        "Tweet": tweet.text,
                        "Sentiment": analyze_sentiment(tweet.text),
                    })
                next_token = response.meta.get("next_token", None)  # Update token for the next page
                if not next_token:  # No more pages
                    break
            else:
                break
        except Exception as e:
            print(f"Error fetching tweets: {e}")
            break

        # Subtract the number of tweets fetched
        remaining_count -= len(response.data)
    
    # Return the data as a Pandas DataFrame
    return pd.DataFrame(tweet_data)
    tweet_data.append({
    "Tweet": tweet.text,
    "Sentiment": analyze_sentiment(tweet.text),  # Analyze sentiment here
})


#Plot sentiment distribution
def plot_sentiment_distribution(data):
    sentiment_counts = data['Sentiment'].value_counts()
    sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red', 'purple'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()

# Main function
def main():
    keyword = input("Enter a fashion-related keyword to search: ")
    count = int(input("Enter the number of tweets to fetch: "))
    print("Fetching tweets...")

    # Fetch tweets and return as a DataFrame
    data = fetch_tweets(keyword, count)

    if not data.empty:  # Check if DataFrame is not empty
        # Display the first few rows
        print(data.head())

        # Plot sentiment distribution
        plot_sentiment_distribution(data)
    else:
        print("No tweets found or an error occurred.")

query = f"{keyword} -is:retweet"



if __name__ == "__main__":
    main()
