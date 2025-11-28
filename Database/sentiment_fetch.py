from google_news_api.client import GoogleNewsClient
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Tuple
import itertools
import tomllib
from datetime import datetime
import requests
import pandas as pd

def parse_clue_dict(source: Dict[str, List[str]]) -> Dict[str, str]:
    return {keyword:ticker for ticker, keywords in source.items() for keyword in keywords }


class News:
    def __init__(
            self,
            title: str,
            description: Optional[str] = None,
            content: Optional[str] = None,
            url: Optional[str] = None,
            source: Optional[str] = None,
            publish_date: Optional[datetime] = None, 
            tickers: Optional[List[str]] = None,
            sentiment_score: Optional[Dict[str, float]] = None
            ):
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.source = source
        self.publish_date = publish_date
        self.tickers = tickers
        self.sentiment_score = sentiment_score
        self.clear_list = ['-', '.', ',', ':']

    def __hash__(self):
        return hash(f"{self.title}-{self.source}")

    def __repr__(self):
        return f"{self.source}: {self.title}"

    def get_ticker_relevance(self, clues: Dict[str, str]) -> Optional[List[str]]:
        parse_title = self.title.translate(str.maketrans({symbol:'' for symbol in self.clear_list})).split(' ')

        score = dict()
        for word in parse_title:
            clue = clues.get(word)
            if clue:
                if score.get(clue) is None:
                    score[clue] = 0
                score[clue] += 1

        kill_yourself = [key for key, val in score.items() if val > 0]
        if len(kill_yourself) == 0:
            return None

        self.tickers = kill_yourself

        return kill_yourself

class NewsAggregator(ABC):
    @abstractmethod
    def get_news(self, ticker: str, start_date: str = "2023-01-01") -> Optional[List[News]]:
        ...

    def get_news_mt(self, tickers: List[str], start_date: str = "2023-01-01") -> Optional[List[News]]:
        res = [self.get_news(ticker, start_date) for ticker in tickers]
        return list(itertools.chain.from_iterable(res))

class GoogleNews(NewsAggregator):
    def __init__(self):
        self.client = GoogleNewsClient()

    def get_news(self, ticker: str, start_date: str = "2023-01-01") -> List[News]: 
        news = self.client.search(ticker, after=start_date)
        return [News(
            title = piece["title"],
            url = piece["link"],
            publish_date = piece["published"],
            source = piece["source"],
            tickers = [ticker],
            ) for piece in news]

class AlphaVantage(NewsAggregator):
    def __init__(self, api_key: str):
        self.link = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}&limit=500"

    def get_news(self, ticker: str, start_date: str = "2023-01-01") -> Optional[List[News]]:
        start_date = start_date.replace('-', '') + "T0000"
        url = self.link + f"&ticker={ticker}&time_from={start_date}"
        print(f"Getting news for query: {url}")
        response = requests.get(url) 

        if response.status_code != 200:
            print("Warning: Non-zero status code for AlphaVantage")
            return None

        content = response.json().get("feed")
        if content is None:
            print(response.json())
            return None

        return [News(
            title = piece["title"],
            source = piece["source"],
            sentiment_score = {part["ticker"]:part["ticker_sentiment_score"] for part in piece["ticker_sentiment"]},
            description = piece["summary"],
            url = piece["url"],
            publish_date = piece["time_published"],
            ) for piece in content]

    def get_news_mt(self, tickers: List[str], start_date: str = "2023-01-01") -> Optional[List[News]]:
        res = []
        for ticker in tickers:
            resp = self.get_news(ticker, start_date)
            if resp is None:
                break

            res.extend(resp)

        if len(res) == 0:
            return None

        return res

def av_to_pandas(source: List[News]) -> pd.DataFrame:
    records = [(record.title, record.url, record.source, record.description, ticker, val) for record in source for ticker, val in record.sentiment_score.items()]
    return pd.DataFrame.from_records(records, columns=["Title", "URL", "Source", "Summary", "Ticker", "Sentiment"])


def main():
    with open("config.toml", "rb") as file:
        config = tomllib.load(file)

    tickers = config["tickers"]["ticker_list"]
    #google = GoogleNews()
    #news = google.get_news_mt(tickers)
    #assert news is not None
    #clue_dict = parse_clue_dict(config["tickers"]["clues"])
    #news = [new for new in news if new.get_ticker_relevance(clue_dict) is not None]
    av_client = AlphaVantage(config["news_apis"]["alpha_vantage"]["key"])
    av_news = av_client.get_news_mt(tickers)
    assert av_news is not None
    #news.extend(av_news)
    #print(news)
    data = av_to_pandas(av_news)
    print(data)



if __name__ == "__main__":
    main()
