from google_news_api.client import GoogleNewsClient
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import itertools
import tomllib
import re
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

def eval_correctness(url):
    return not any(part in url for part in ["google.com", "consent", "Consent", "guce.yahoo.com"])

class GoogleNews(NewsAggregator):
    def __init__(self):
        self.client = GoogleNewsClient()

    def get_news(self, ticker: str, start_date: str = "2023-01-01", ban_list: List[str] = [], build_limit: Optional[int] = None) -> List[News]: 

        with open("headers.json", "rb") as file:
            headers = json.load(file)
        news = self.client.search(ticker, after=start_date)
        if build_limit:
            if build_limit < len(news):
                news = news[:build_limit]
        if ban_list:
            banned_pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in ban_list) + r')\b', re.IGNORECASE)
            built_news = [ self.build_news(new, headers) for new in news if not banned_pattern.search(new["title"]) ]
        else:
            built_news = [ self.build_news(new, headers) for new in news]
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
        
        to_get = newspaper.Article(url=url)
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
    if source[0].sentiment is None:
        records = [(record.title, record.url, record.source, record.description, record.content, record.publish_date) for record in source]
        cols = ["title", "url", "source", "summary", "text", "date"]
    else:
        records = [(record.title, record.url, record.source, record.description, record.publish_date, record.tickers, record.sentiment) for record in source]
        cols = ["title", "url", "source", "summary", "date", "ticker", "sentiment"]

    return pd.DataFrame.from_records(records, columns=cols)

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
        # The pipeline returns a list of lists of scores when return_all_scores=True
        batch_scores = finbert_pipeline(batch, truncation=True, return_all_scores=True)

        for score_list in batch_scores:
            scores = {item['label']: item['score'] for item in score_list}
            # The score is calculated as P(positive) - P(negative)
            # FinBERT labels are 'positive', 'negative', 'neutral'
            sentiment_score = scores.get('positive', 0.0) - scores.get('negative', 0.0)

            if sentiment_score >= 0.35:
                label = 'Bullish'
            elif sentiment_score >= 0.15:
                label = 'Somewhat-Bullish'
            elif sentiment_score > -0.15:
                label = 'Neutral'
            elif sentiment_score > -0.35:
                label = 'Somewhat-Bearish'
            else:
                label = 'Bearish'

            results.append({'sentiment_score': sentiment_score, 'sentiment_label': label})
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
    data = data.sort_values(by=["url"]).drop_duplicates().sort_values(by=["ticker"])
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
        print(ban_list := config["tickers"]["ban_list"]["IWM"])
        news = google.get_news(tickers[0], ban_list = ban_list, build_limit=10)
        assert news is not None

        data = gn_to_pandas(news)
        data.to_csv("google_data.csv", index = False)
    else:
        data = pd.read_csv("google_data.csv")
        print(data)
        records = data.to_records(index = False) 
        if len(records[0]) == 6:
            to_news = lambda x: News(title = x[0], url = x[1], source = x[2], description = x[3], content = x[4], publish_date = x[5])
        else:
            to_news = lambda x: News(title = x[0], url = x[1], source = x[2], description = x[3], content = x[4], publish_date = x[5], sentiment = x[6])
        news = [to_news(record) for record in data.to_records(index = False)]
    #print(google.client.search("AAPL", after = "2023-01-01")[0])
    clue_dict = parse_clue_dict(config["tickers"]["clues"])
    news = [new for new in news if new.get_ticker_relevance(clue_dict) is not None]
    print(f"IMPORTANT: [new.tickers for new in news]")
    print("Done. Moving to sentiment processing.")
    #news = list(set(news))
    print(news)

    scores = batch_process_sentiment(news)

    for new, score in zip(news, scores):
        score_num = score["sentiment_score"]
        new.sentiment = score_num

    data = gn_to_pandas(news)

    data = data.sort_values(by=["url"]).drop_duplicates(subset=["url"]).sort_values(by=["ticker"])

    print(data)

    conn_conf = config["database"]

    sql_engine = create_engine(f'postgresql://{conn_conf["user"]}:{conn_conf["password"]}@{conn_conf["host"]}:{conn_conf["port"]}/{conn_conf["dbname"]}')

    dupes = pd.read_sql("SELECT url FROM sentiment_pieces", sql_engine)
    data = remove_dupes(data, dupes)
    print(data)

    #data.to_sql("sentiment_pieces", sql_engine, if_exists = "append", index = False)

def get_google_news(config, tickers):
    google = GoogleNews()
    ban_list = config["tickers"]["ban_list"]["IWM"]
    conn_conf = config["database"]
    sql_engine = create_engine(f'postgresql://{conn_conf["user"]}:{conn_conf["password"]}@{conn_conf["host"]}:{conn_conf["port"]}/{conn_conf["dbname"]}')

    for ticker in tickers:
        news = google.get_news(ticker, ban_list = ban_list)
        assert news is not None

        clue_dict = parse_clue_dict(config["tickers"]["clues"])
        news = [new for new in news if new.get_ticker_relevance(clue_dict) is not None]
        assert news is not None

        scores = batch_process_sentiment(news)
        for new, score in zip(news, scores):
            score_num = score["sentiment_score"]
            new.sentiment = score_num

        data = gn_to_pandas(news)
        data = data.sort_values(by=["url"]).drop_duplicates(subset=["url"]).sort_values(by=["ticker"])

        dupes = pd.read_sql("SELECT url FROM sentiment_pieces", sql_engine)
        data = remove_dupes(data, dupes)

        data.to_sql("sentiment_pieces", sql_engine, if_exists = "append", index = False)

def get_google_headlines(tickers: List[str]):
    client = GoogleNewsClient()
    data = []
    for ticker in tickers:
        data_part = client.search(ticker, after = "2023-01-01")

        data_part = [new["title"] for new in data_part]
        data.extend(data_part)

    print(len(data))

def main():
    with open("config.toml", "rb") as file:
        config = tomllib.load(file)

    tickers = config["tickers"]["ticker_list"]
    #get_google_news(config, tickers)
    google_news_test(config, tickers)

if __name__ == "__main__":
    main()
