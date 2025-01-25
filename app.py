from flask import Flask, request, jsonify
import tweepy
from textblob import TextBlob
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Twitter API keys
API_KEY = ' ozKt5YERur47qAFL4jmOKvXBj'
API_SECRET = '99ccay4ayN8cAY9XXVgEPrWZjuf1bsqGwGboEkAOotk2U6MfcD'
ACCESS_TOKEN = '1649847772835635202-Sxt7DRw19b4BJjMqXRqqKZ50WfFUb7'
ACCESS_SECRET = 'zNupF0oMtAzQeI5i8pMR5KAfebCWAtOkCv5ANbV8aDHvO'

# Set up Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Sentiment Analysis Endpoint
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        query = data.get('query', '')
        logging.info(f"Fetching tweets for query: {query}")
        
        tweets = api.search_tweets(q=query, count=100, lang='en')
        sentiments = {"positive": 0, "negative": 0, "neutral": 0, "sarcastic": 0}

        for tweet in tweets:
            analysis = TextBlob(tweet.text)
            if analysis.sentiment.polarity > 0:
                sentiments["positive"] += 1
            elif analysis.sentiment.polarity < 0:
                sentiments["negative"] += 1
            else:
                sentiments["neutral"] += 1

            # Example: Sarcasm detection (custom logic)
            if "not" in tweet.text.lower() and analysis.sentiment.polarity > 0:
                sentiments["sarcastic"] += 1

        return jsonify(sentiments)

    except tweepy.TweepError as e:
        logging.error(f"Twitter API error: {e}")
        return jsonify({"error": "Failed to fetch tweets. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=True)
