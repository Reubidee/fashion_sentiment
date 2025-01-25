from flask import Flask, request, jsonify
from transformers import pipeline
import tweepy

app = Flask(__name__)

# Set up sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis")

# Set up Twitter API (use your BEARER_TOKEN)
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEJZwgEAAAAAD4pkPk72wm939DsoCRAUtpuIzDs%3Dh9p7X9icXrc9uZvzeeZKvFPuqjC9E0CWyYSEqu41FbANpM7oi9"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_tweets(query, max_results):
    try:
        response = client.search_recent_tweets(query=query, max_results=max_results, tweet_fields=["text", "lang"])
        tweets = [tweet.text for tweet in response.data if tweet.lang == "en"]
        return tweets
    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return []

@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    data = request.json
    keyword = data.get("keyword")
    max_results = int(data.get("max_results", 10))
    
    query = f"{keyword} -is:retweet"
    tweets = fetch_tweets(query, max_results)
    sentiments = [{"tweet": tweet, "sentiment": sentiment_pipeline(tweet)[0]["label"]} for tweet in tweets]
    return jsonify(sentiments)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
