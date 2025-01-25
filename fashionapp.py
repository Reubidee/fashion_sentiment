from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Assuming your fetch_tweets and analyze_sentiment functions are already defined
from fashion_sentiment import fetch_tweets

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({"message": f"Received POST request with data: {data}"})
    return "Welcome to the Fashion Sentiment Analysis API!"


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    try:
        # Get data from the request
        data = request.get_json()
        keyword = data.get('keyword')
        count = data.get('count', 20)

        if not keyword:
            return jsonify({'error': 'Keyword is required'}), 400

        # Fetch tweets and analyze
        tweets = fetch_tweets(keyword, count)

        if not tweets:
            return jsonify({'error': 'No tweets found for the given keyword.'}), 404

        df = pd.DataFrame(tweets)
        df['Sentiment'] = df['Text'].apply(analyze_sentiment)  # Assuming you have this function

        # Sentiment distribution
        sentiment_counts = df['Sentiment'].value_counts()

        # Plot sentiment distribution
        fig, ax = plt.subplots()
        sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red'], ax=ax)
        ax.set_title('Sentiment Analysis')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')

        # Convert plot to image
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return jsonify({
            'sentiment_counts': sentiment_counts.to_dict(),
            'plot_url': f'data:image/png;base64,{plot_url}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from textblob import TextBlob

def detect_sarcasm(text):
    # Example rule-based sarcasm detection
    if "yeah right" in text.lower() or "sure, as if" in text.lower():
        return True
    return False

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if detect_sarcasm(text):
        return "Sarcastic"
    elif sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

import matplotlib.pyplot as plt

def plot_sentiment_distribution(data):
    sentiment_counts = data['Sentiment'].value_counts()
    sentiment_counts.plot(kind='bar', color=['green', 'blue', 'red', 'purple'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()

