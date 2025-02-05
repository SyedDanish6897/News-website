from flask import Flask, render_template, jsonify
from newsapi import NewsApiClient

app = Flask(__name__)

# API Key
API_KEY = '25560f3cf53c433c9807c60595b373a6'
newsapi = NewsApiClient(api_key=API_KEY)

@app.route("/")
def home():
    # Fetch 10 top headlines + 10 more from everything (to ensure at least 15 articles)
    top_headlines = newsapi.get_top_headlines(sources="bbc-news", page_size=10)
    all_articles = newsapi.get_everything(sources="bbc-news", page_size=10)

    articles = top_headlines['articles'] + all_articles['articles']

    # Remove duplicates by checking unique URLs
    unique_articles = {article['url']: article for article in articles}.values()

    # Limit to 15 articles
    contents = [{
        'title': article['title'],
        'description': article['description'] if article['description'] else "No description available.",
        'image': article['urlToImage'] if article['urlToImage'] else "/static/img/default-news.jpg",
        'published_at': article['publishedAt'],
        'url': article['url']
    } for article in unique_articles][:15]  # Ensure only 15 articles

    return render_template('newsweb.html', contents=contents)

@app.route("/fetch_news")
def fetch_news():
    # Fetch latest news dynamically
    top_headlines = newsapi.get_top_headlines(sources="bbc-news", page_size=10)
    all_articles = newsapi.get_everything(sources="bbc-news", page_size=10)

    articles = top_headlines['articles'] + all_articles['articles']

    # Remove duplicates and ensure 15 articles
    unique_articles = {article['url']: article for article in articles}.values()
    
    news_data = [{
        'title': article['title'],
        'description': (article['description'][:150] + "... <a href='" + article['url'] + "' style='color:yellow;'>Read More</a>") 
                        if article['description'] and len(article['description']) > 150 else article['description'] or "No description available.",
        'image': article['urlToImage'] if article['urlToImage'] else "/static/img/default-news.jpg",
        'published_at': article['publishedAt'],
        'url': article['url']
    } for article in unique_articles][:15]  # Ensure only 15 articles

    return jsonify(news_data)

if __name__ == '__main__':
    app.run(debug=True)
