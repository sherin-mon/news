import requests
from flask import Flask, jsonify, send_from_directory
import os
import logging

# Remove dotenv loading for Kubernetes setup
# load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# News API setup
NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # This will get the value from Kubernetes secret
if not NEWS_API_KEY:
    logger.error("NEWS_API_KEY is not set. Please ensure it is provided as an environment variable.")
    exit(1)

NEWS_API_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'

@app.route('/')
def get_news():
    try:
        response = requests.get(NEWS_API_URL)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get('articles', [])
        news = [{'title': article.get('title', 'No Title'), 'description': article.get('description', 'No Description')} 
                for article in articles]
        return jsonify(news)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news data: {e}")
        return jsonify({'error': 'Failed to fetch news data'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

