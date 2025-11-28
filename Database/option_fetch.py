import concurrent.futures as cf
import yfinance as yf
from typing import List, Tuple
import logging
import time
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import tomllib

THREAD_LIMIT = 4

def parse_ticker_names(path: str = "") -> List[str]:
    assert path != "", "Empty path."
    with open(path, "r") as file:
        tickers_raw = file.readlines()

    for index, ticker in enumerate(tickers_raw):
        position = ticker.find('#')
        if position != -1:
            ticker = ticker.split('#')[0]

        tickers_raw[index] = ticker.strip()

    return list(filter(lambda x: bool(x), tickers_raw))

def parse_tickers(preticks: List[str]) -> List[yf.Ticker]:
    return [ yf.Ticker(tick) for tick in preticks ]

def get_relevant_info(ticker: yf.Ticker) -> Tuple[pd.DataFrame, pd.DataFrame] | None:
    #return (ticker.info.get("currentPrice"), ticker.option_chain())
    if len(ticker.options) <= 0:
        print(f"Ticker {ticker.ticker} has no option chains.")
        return None
    print(ticker.ticker)
    option_chain_list = [ ticker.option_chain(date, tz='CET') for date in ticker.options]
    if len(option_chain_list) <= 0:
        print(f"{ticker.ticker} has no option chains, tf?")
        return None
    option_chain_calls = [ oc.calls for oc in option_chain_list ]
    option_chain_puts = [ oc.puts for oc in option_chain_list ]

    for index, date_str in enumerate(ticker.options):
        option_chain_calls[index]["expirationDate"] = datetime.strptime(date_str, "%Y-%m-%d")
        option_chain_calls[index]["ticker"] = ticker.ticker
        option_chain_puts[index]["expirationDate"] = datetime.strptime(date_str, "%Y-%m-%d")
        option_chain_puts[index]["ticker"] = ticker.ticker

    return (pd.concat(option_chain_calls, ignore_index = True), pd.concat(option_chain_puts, ignore_index = True))

def main():
    with open("config.toml", "rb") as file:
        config = tomllib.load(file)
    tickers = parse_tickers(config["tickers"]["ticker_list"])

    conn_conf = config["database"]
    sql_engine = create_engine(f'postgresql://{conn_conf["user"]}:{conn_conf["password"]}@{conn_conf["host"]}:{conn_conf["port"]}/{conn_conf["dbname"]}')
    try:
        with cf.ThreadPoolExecutor(max_workers = THREAD_LIMIT) as thread_pool:
            while True:
                start_time = time.time()

                futures = [ thread_pool.submit(get_relevant_info, ticker) for ticker in tickers ]

                results = [ future.result() for future in futures ]
                print(results)

                calls = [ result[0] for result in results if result ]
                puts = [ result[1] for result in results if result ]

                update_time = datetime.now()
                calls_final = pd.concat(calls, ignore_index = True)
                calls_final["uploadTime"] = update_time
                calls_final["inTheMoney"] = calls_final["inTheMoney"] == 1.0
                puts_final = pd.concat(puts, ignore_index = True)
                puts_final["uploadTime"] = update_time
                puts_final["inTheMoney"] = puts_final["inTheMoney"] == 1.0

                print(calls_final.columns)
                print(calls_final.dtypes)
                print(set(calls_final["inTheMoney"].to_list()))

                calls_final.to_sql(name = "calls", con = sql_engine, index = False, if_exists="append")
                puts_final.to_sql(name = "puts", con = sql_engine, index = False, if_exists="append")

                end_time = time.time()
                time_diff = 60 - (end_time - start_time)
                print(time_diff)
                if time_diff <= 0:
                    continue
                time.sleep(time_diff)

    except KeyboardInterrupt as _:
        print("Detected a keyboard interrupt. Gracefully exiting.")
    except Exception as err:
        print(f"Found an unknown error: {err}")
        return
    
if __name__ == "__main__":
    main()
