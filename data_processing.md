    library(readr)
    library(dplyr)

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

# Načtení stock price dat

    stock_jan <- read_csv("Data_fetch/stock_prices_2026-01-26.csv")

    ## Rows: 4523 Columns: 9
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (1): Ticker
    ## dbl  (7): Open, High, Low, Close, Volume, Dividends, Stock Splits
    ## dttm (1): Date
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    stock_feb <- read_csv("Data_fetch/stock_prices_2026-02-27.csv")

    ## Rows: 4523 Columns: 9
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (1): Ticker
    ## dbl  (7): Open, High, Low, Close, Volume, Dividends, Stock Splits
    ## dttm (1): Date
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    stock_mar <- read_csv("Data_fetch/stock_prices_2026-03-27.csv")

    ## Rows: 4519 Columns: 9
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (1): Ticker
    ## dbl  (7): Open, High, Low, Close, Volume, Dividends, Stock Splits
    ## dttm (1): Date
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    stock_may <- read_csv("Data_fetch/stock_prices_2026-05-26.csv")

    ## Rows: 4518 Columns: 9
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr  (1): Ticker
    ## dbl  (7): Open, High, Low, Close, Volume, Dividends, Stock Splits
    ## dttm (1): Date
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    stock_jan$Date <- as.Date(stock_jan$Date)
    stock_feb$Date <- as.Date(stock_feb$Date)
    stock_mar$Date <- as.Date(stock_mar$Date)
    stock_may$Date <- as.Date(stock_may$Date)

# Výpočet S\_no\_dividend

    calc_S_no_dividend <- function(df) {
      df %>%
        group_by(Ticker) %>%
        summarise(
          current_price = last(Close),
          total_divs = sum(Dividends, na.rm = TRUE),
          S_no_dividend = current_price + total_divs
        )
    }

    s_no_div_jan <- calc_S_no_dividend(stock_jan)
    s_no_div_feb <- calc_S_no_dividend(stock_feb)
    s_no_div_mar <- calc_S_no_dividend(stock_mar)
    s_no_div_may <- calc_S_no_dividend(stock_may)

# Funkce pro výpočet T

    calc_T <- function(origin_date, expirations) {
      data.frame(expiration = expirations) %>%
        mutate(T = (as.numeric(as.Date(expiration) - origin_date) + 1) / 365)
    }

# Funkce pro enrichment options dat

    enrich_options <- function(options_df, origin_date, s_no_div_df, style) {
      unique_expirations <- unique(options_df$expiration)
      t_df <- calc_T(origin_date, unique_expirations)

      options_df %>%
        left_join(s_no_div_df, by = c("ticker" = "Ticker")) %>%
        left_join(t_df, by = "expiration") %>%
        mutate(
          pomer_K_S = K / S,
          option_style = style
        )
    }

# Načtení options dat

    am_jan <- read_csv("Data_fetch/american_options_2026-01-26_greeks.csv")

    ## Rows: 35701 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    am_feb <- read_csv("Data_fetch/american_options_2026-02-27_greeks.csv")

    ## Rows: 36824 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    am_mar <- read_csv("Data_fetch/american_options_2026-03-27_greeks.csv")

    ## Rows: 35785 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    eu_jan <- read_csv("Data_fetch/european_options_2026-01-26_greeks.csv")

    ## Rows: 5511 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    eu_feb <- read_csv("Data_fetch/european_options_2026-02-27_greeks.csv")

    ## Rows: 4965 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    eu_mar <- read_csv("Data_fetch/european_options_2026-03-27_greeks.csv")

    ## Rows: 5174 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    am_may <- read_csv("Data_fetch/american_options_2026-05-26_greeks.csv")

    ## Rows: 39090 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

    eu_may <- read_csv("Data_fetch/european_options_2026-05-26_greeks.csv")

    ## Rows: 5946 Columns: 13
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr   (2): ticker, option_type
    ## dbl  (10): K, bid_price, ask_price, option_price, volume, open_interest, r, ...
    ## date  (1): expiration
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

# Enrichment

    origin_jan <- as.Date("2026-01-26")
    origin_feb <- as.Date("2026-02-27")
    origin_mar <- as.Date("2026-03-27")
    origin_may <- as.Date("2026-05-26")

    am_jan <- enrich_options(am_jan, origin_jan, s_no_div_jan, "American")
    am_feb <- enrich_options(am_feb, origin_feb, s_no_div_feb, "American")
    am_mar <- enrich_options(am_mar, origin_mar, s_no_div_mar, "American")

    eu_jan <- enrich_options(eu_jan, origin_jan, s_no_div_jan, "European")
    eu_feb <- enrich_options(eu_feb, origin_feb, s_no_div_feb, "European")
    eu_mar <- enrich_options(eu_mar, origin_mar, s_no_div_mar, "European")

    am_may <- enrich_options(am_may, origin_may, s_no_div_may, "American")
    eu_may <- enrich_options(eu_may, origin_may, s_no_div_may, "European")

# Sloučení a uložení

    american_all <- bind_rows(am_jan, am_feb, am_mar, am_may)
    european_all <- bind_rows(eu_jan, eu_feb, eu_mar, eu_may)

    just_all <- bind_rows(american_all, european_all)

    selection <- c(
      "ticker",
      "expiration",
      "S",
      "K",
      "r",
      "sigma",
      "T",
      "option_price",
      "pomer_K_S",
      "option_style",
      "option_type",
      "S_no_dividend",
      "q"
    )

    just_all <- just_all[selection]

    write_csv(american_all, "Data_fetch/american_options_all.csv")
    write_csv(european_all, "Data_fetch/european_options_all.csv")

    write_csv(just_all, "Data_fetch/complete_dataset.csv")

    cat("American options:", nrow(american_all), "rows\n")

    ## American options: 147400 rows

    cat("European options:", nrow(european_all), "rows\n")

    ## European options: 21596 rows
