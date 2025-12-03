from google_news_api.client import GoogleNewsClient
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import itertools
import tomllib
from datetime import datetime
import requests
import pandas as pd
import newspaper
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch
from redirect_resolver import get_final_url_from_google 
import json
import logging
import os.path
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

logging.basicConfig(filename="wtf.log", level=logging.INFO)

def parse_clue_dict(source: Dict[str, List[str]]) -> Dict[str, str]:
    return {keyword:ticker for ticker, keywords in source.items() for keyword in keywords }

# The `requests` library automatically handles decompression (e.g., zstd, gzip),
# so manual decoding is not required. Accessing `response.text` provides the
# decoded content directly.
#
# def decode_content(content: bytes, encoding: Optional[str]) -> str:
#     if not encoding or encoding.lower() == "identity":
#         return content.decode("utf-8")
# 
#     match encoding.lower():
#         case "zstd":
#             return zstd.decompress(content).decode("utf-8")
#         case "gzip":
#             return gzip.decompress(content).decode("utf-8")
#         case _:
#             raise ValueError(f"Unsupported encoding: {encoding}")

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
            sentiment_score: Optional[Dict[str, float]] = None,
            sentiment: Optional[str] = None,
            sentiment_confidence: Optional[str] = None,
            ):
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.source = source
        self.publish_date = publish_date
        self.tickers = tickers
        self.sentiment_score = sentiment_score
        self.sentiment = sentiment
        self.sentiment_confidence = sentiment_confidence

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
        print(kill_yourself)
        if len(kill_yourself) == 0:
            return None

        self.tickers = kill_yourself

        return kill_yourself

    def set_ticker(self, ticker):
        self.tickers = [ticker]
        return self

class NewsAggregator(ABC):
    @abstractmethod
    def get_news(self, ticker: str, start_date: str = "2023-01-01") -> Optional[List[News]]:
        ...

    def get_news_mt(self, tickers: List[str], start_date: str = "2023-01-01") -> Optional[List[News]]:
        res = []
        for ticker in tickers:
            preres = self.get_news(ticker, start_date) 
            res.extend(prepres)
        return res

eval_correctness = lambda url: not any(part in url for part in ["google.com", "consent", "Consent", "guce.yahoo.com"])

class GoogleNews(NewsAggregator):
    def __init__(self):
        self.client = GoogleNewsClient()

    def get_news(self, ticker: str, start_date: str = "2023-01-01", ban_list: List[str] = []) -> List[News]: 
        with open("headers.json", "rb") as file:
            headers = json.load(file)
        news = self.client.search(ticker, after=start_date)
        if len(news) > 5:
            max_len = 5
        else:
            max_len = len(news)
        built_news = [ self.build_news(new, headers) for new in news[:max_len] if not any([word.lower() in new["title"] for word in ban_list]) ]
        print(built_news)
        return [bn for bn in built_news if bn is not None]

    def get_news_mt(self, tickers: List[str], start_date: str = "2023-01-01", ban_list: Dict[str, List[str]] = dict()) -> Optional[List[News]]:
        res = [self.get_news(ticker, start_date, ban_list.get(ticker, [])) for ticker in tickers]
        return list(itertools.chain.from_iterable(res))

    def build_news(self, article: Dict[str, Any], headers) -> Optional[News]:
        print(f"Building {article['title']}")
        url = article.get("link")
        content = None
        assert url
        while not eval_correctness(url):
            print("One of url conditions not met.")
            url, content = get_final_url_from_google(url)
            if content:
                break
            if not url:
                raise ConnectionError("Could not resolve url")

        assert url
        
        if content is None:
            headers["Host"] = url.split('/')[2]
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            content = resp.content

        logger.info(f"URL: {url}")
        
        #print(f"Content-Encoding: {content_encoding}")
        print(f"Content length after decompression: {len(content)}")
        logger.info(f"Post-compression: {content}")
        to_get = newspaper.Article(url=url)
        #to_get.download()
        to_get.set_html(content)
        to_get.parse()
        to_get.nlp()

        if len(to_get.text) == 0:
            print(f"Warning: newspaper could not extract text from {url}")
            return None
        
        return News(
            title = article["title"],
            url = article["link"],
            publish_date = article["published"],
            source = article["source"],
            description = to_get.summary,
            content = to_get.text
                )

class AlphaVantage(NewsAggregator):
    def __init__(self, api_key: str):
        self.link = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}&limit=1000"

    def get_news(self, ticker: str, start_date: str = "2023-01-01") -> Optional[List[News]]:
        start_date = start_date.replace('-', '') + "T0000"
        url = self.link + f"&tickers={ticker}&time_from={start_date}"
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
            publish_date = datetime.fromisoformat(piece["time_published"]),
            ) for piece in content]



    def get_news_mt(self, tickers: List[str], start_date: str = "2023-01-01") -> Optional[List[News]]:
        res = []
        for ticker in tickers:
            resp = self.get_news(ticker, start_date)
            if resp is None:
                break

            print(resp[:50])
            print(len(resp))

            res.extend(resp)

        if len(res) == 0:
            return None

        return res

def av_to_pandas(source: List[News], tickers: List[str]) -> pd.DataFrame:
    records = [(record.title, record.url, record.source, record.description, ticker, val, record.publish_date) for record in source for ticker, val in record.sentiment_score.items()]
    data = pd.DataFrame.from_records(records, columns=["title", "url", "source", "summary", "ticker", "sentiment", "date"])
    return data

def gn_to_pandas(source: List[News]) -> pd.DataFrame:
    records = [(record.title, record.url, record.source, record.description, record.content, record.publish_date) for record in source]
    return pd.DataFrame.from_records(records, columns=["title", "url", "source", "summary", "text", "date"])

def batch_process_sentiment(news: List[News]):
    batch_size = 8

    # Load FinBERT model and tokenizer
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Create sentiment analysis pipeline
    finbert_pipeline = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )

    texts = [new.content or "" for new in news]
    print(texts)
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_results = finbert_pipeline(batch, truncation=True)
        for result in batch_results:
            sentiment_map = {"positive": "bullish", "negative": "bearish"}
            label = result["label"]
            sentiment = sentiment_map.get(label, label)
            results.append({"sentiment": sentiment, "confidence": result["score"]})
    return results

def remove_dupes(self: pd.DataFrame, other: pd.DataFrame) -> pd.DataFrame:
    outer = self.merge(other, how = 'outer', on = "url", indicator = True)

    return outer[(outer._merge=='left_only')].drop('_merge', axis=1)

DATA_WRITE_LOC = "alpha_vantage_data.csv"

def av_test_read(config, tickers):
    print("Fetching news...")
    av_client = AlphaVantage(config["news_apis"]["alpha_vantage"]["key"])
    av_news = av_client.get_news_mt(tickers)
    assert av_news is not None
    data = av_to_pandas(av_news,tickers)
    print(data)
    data = data.drop_duplicates(subset=["url"])
    data.to_csv(DATA_WRITE_LOC, index = False)

def av_test_write(config, tickers):
    if not os.path.isfile(DATA_WRITE_LOC):
        print("No test file found, running read test first.")
        av_test_read(config, tickers)
    data = pd.read_csv(DATA_WRITE_LOC)
    data = data[data["ticker"].isin(tickers)]
    data = data.sort_values(by=["url"]).drop_duplicates(subset=["url"]).sort_values(by=["ticker"])

    print(data)

    conn_conf = config["database"]

    sql_engine = create_engine(f'postgresql://{conn_conf["user"]}:{conn_conf["password"]}@{conn_conf["host"]}:{conn_conf["port"]}/{conn_conf["dbname"]}')

    dupes = pd.read_sql("SELECT url FROM sentiment_pieces", sql_engine)
    data = remove_dupes(data, dupes)
    print(data)

    data.to_sql("sentiment_pieces", sql_engine, if_exists = "append", index = False)

def google_news_test(config, tickers):
    print("Fetching news...")
    if not os.path.isfile("google_data.csv"):
        google = GoogleNews()
        news = google.get_news(tickers[0], ban_list = config["tickers"]["ban_list"]["IWM"])
        assert news is not None

        data = gn_to_pandas(news)
        data.to_csv("google_data.csv", index = False)
    else:
        data = pd.read_csv("google_data.csv")
        print(data)
        to_news = lambda x: News(title = x[0], url = x[1], source = x[2], description = x[3], content = x[4], publish_date = x[5])
        news = [to_news(record) for record in data.to_records(index = False)]
    #print(google.client.search("AAPL", after = "2023-01-01")[0])
    clue_dict = parse_clue_dict(config["tickers"]["clues"])
    news = [new for new in news if new.get_ticker_relevance(clue_dict) is not None]
    print("Done. Moving to sentiment processing.")
    #news = list(set(news))
    print(news)

    print(batch_process_sentiment(news))


def main():
    with open("config.toml", "rb") as file:
        config = tomllib.load(file)

    tickers = config["tickers"]["ticker_list"]
    google_news_test(config, tickers)
    #av_test_write(config, tickers)

if __name__ == "__main__":
    main()
