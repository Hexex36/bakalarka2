import google_news_api as gna

client = gna.GoogleNewsClient()

news = client.search("AAPL")

print(news)
