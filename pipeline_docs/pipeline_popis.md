# Pipeline zpracování dat (Data_fetch → complete_dataset)

## Přehled

Pipeline transformuje surová options data z Yahoo Finance do finálního datasetu
připraveného pro analýzu (Black-Scholes, fitting atd.).

Skládá se ze 4 kroků:

```
Raw CSV (options, stock, rates)
        │
        ▼  rate_functioner_complete.py  (krok 2)
  *_enhanced.csv
        │
        ▼  rename_to_greeks.py          (krok 3)
  *_greeks.csv
        │
        ▼  data_processing.rmd          (krok 4)
  *_options_all.csv  +  complete_dataset.csv
```

---

## Struktura souborů

### Surová data (vstup)

| Soubor | Popis |
|---|---|
| `american_options_YYYY-MM-DD.csv` | Americké opce (stock tickery) z Yahoo Finance |
| `european_options_YYYY-MM-DD.csv` | Evropské opce (index tickery) z Yahoo Finance |
| `stock_prices_YYYY-MM-DD.csv` | Denní ceny akcií + dividendy (1 rok historie) |
| `rates_YYYY_MM_DD.txt` | Treasury výnosová křivka (US Treasury) |

### Mezikroky

| Soubor | Popis |
|---|---|
| `*_enhanced.csv` | Options + treasury_rate + current_stock_price + sigma + q |
| `*_greeks.csv` | Enhanced s přejmenovanými sloupci (K, S, r, sigma, q...) |
| `*_with_rates.csv` | (Starší formát) Jen rate, bez stock dat |

### Finální dataset

| Soubor | Popis |
|---|---|
| `american_options_all.csv` | Všechny americké opce napříč měsíci (rozšířené) |
| `european_options_all.csv` | Všechny evropské opce napříč měsíci (rozšířené) |
| `complete_dataset.csv` | Spojené + ořezané na potřebné sloupce |

---

## Kroky podrobně

### Krok 1: Fetch (stažení surových dat)

Tři nezávislé skripty — spouští se v libovolném pořadí:

```bash
source .venv/bin/activate

# 1a) Options chainy
python options_fetcher_final.py
# Vytvoří: american_options_YYYY-MM-DD.csv, european_options_YYYY-MM-DD.csv

# 1b) Stock prices (1 rok historie)
python price_fetcher.py
# Vytvoří: stock_prices_YYYY-MM-DD.csv

# 1c) Rate (STÁHNOUT MANUÁLNĚ z US Treasury)
# https://home.treasury.gov/resource-center/data-chart-center/interest-rates/
# Uložit jako: rates_YYYY_MM_DD.txt
# Formát: date,1m,1.5m,2m,3m,4m,6m,1y,2y,3y,5y,7y,10y,20y,30y
#          MM/DD/YYYY,3.74,3.73,...
```

### Krok 2: Enhanced options (rates + stock data)

**Skript:** `rate_functioner_complete.py`

Třída `EnhancedOptionsProcessor`:
1. `RateFuncer` — načte rates, interpoluje treasury rate pro každou expiraci
2. `StockPriceVolatilityCalculator` — spočítá `S` (poslední cena), `sigma` (historická vola, 252d), `q` (dividend yield)

**Přidání nového měsíce:** Do `__main__` sekce přidat nový záznam:

```python
{
    "rates_file": "rates_2026_05_26.txt",
    "stock_file": "stock_prices_2026-05-26.csv",
    "target_date": "2026-05-26",
    "date_suffix": "2026-05-26",
},
```

Spuštění:

```bash
source .venv/bin/activate
python rate_functioner_complete.py
```

Vytvoří:
- `american_options_2026-05-26_enhanced.csv`
- `european_options_2026-05-26_enhanced.csv`

**Sloupce enhanced:** `Ticker, Expiration, strike, Type, bid, ask, lastPrice, volume, openInterest, treasury_rate, current_stock_price, historical_volatility, dividend_yield`

### Krok 3: Přejmenování na Greek notaci

**Skript:** `rename_to_greeks.py`

Mapování sloupců:
| Původní | Greek |
|---|---|
| `strike` | `K` |
| `lastPrice` | `option_price` |
| `bid` / `ask` | `bid_price` / `ask_price` |
| `historical_volatility` | `sigma` |
| `treasury_rate` | `r` |
| `current_stock_price` | `S` |
| `dividend_yield` | `q` |
| `Ticker` | `ticker` |
| `Expiration` | `expiration` |
| `Type` | `option_type` |
| `volume` | `volume` |
| `openInterest` | `open_interest` |

**Přidání nového měsíce:** Do `files_to_process` v `main()` přidat:

```python
{
    "input": "./american_options_2026-05-26_enhanced.csv",
    "output": "./american_options_2026-05-26_greeks.csv",
},
{
    "input": "./european_options_2026-05-26_enhanced.csv",
    "output": "./european_options_2026-05-26_greeks.csv",
},
```

Spuštění:

```bash
source .venv/bin/activate
python rename_to_greeks.py
```

### Krok 4: Finální dataset (R)

**Skript:** `data_processing.rmd` (v kořeni projektu, ne v `Data_fetch/`)

Tento R Markdown:
1. Načte stock data → spočítá `S_no_dividend = S + sum(Dividends)` a `total_divs`
2. Načte `*_greeks.csv`
3. Spočítá `T` (trading days / 252 / 52) pro každou expiraci
4. Přidá `pomer_K_S = K / S`
5. Přidá `option_style` (American / European)
6. Sloučí vše do `*_options_all.csv` a `complete_dataset.csv`

**Přidání nového měsíce:**

Do sekce `load_stock_data`:
```r
stock_may <- read_csv("Data_fetch/stock_prices_2026-05-26.csv")
stock_may$Date <- as.Date(stock_may$Date)
```

Do sekce `calc_S_no_dividend`:
```r
s_no_div_may <- calc_S_no_dividend(stock_may)
```

Do sekce `load_options_data`:
```r
am_may <- read_csv("Data_fetch/american_options_2026-05-26_greeks.csv")
eu_may <- read_csv("Data_fetch/european_options_2026-05-26_greeks.csv")
```

Do sekce `enrichment`:
```r
origin_may <- as.Date("2026-05-26")

am_may <- enrich_options(am_may, origin_may, s_no_div_may, stock_may, "American")
eu_may <- enrich_options(eu_may, origin_may, s_no_div_may, stock_may, "European")
```

Do sekce `merge_and_save` přidat do `bind_rows`:
```r
american_all <- bind_rows(am_jan, am_feb, am_mar, am_may)
european_all <- bind_rows(eu_jan, eu_feb, eu_mar, eu_may)
```

Spuštění — buď v RStudiu kliknout na `Knit`, nebo v terminálu:

```bash
Rscript -e "rmarkdown::render('data_processing.rmd')"
```

**Sloupce finálního datasetu:**

| Sloupec | Popis |
|---|---|
| `ticker` | Ticker symbol |
| `expiration` | Datum expirace |
| `S` | Current stock price |
| `K` | Strike price |
| `r` | Risk-free rate (interpolovaná) |
| `sigma` | Historická volatilita (annualizovaná) |
| `T` | Time to expiration (roky, trading days base) |
| `option_price` | lastPrice z Yahoo Finance |
| `pomer_K_S` | K / S poměr |
| `option_style` | American / European |
| `option_type` | Call / Put |
| `S_no_dividend` | S + kumulované dividendy za období |
| `q` | Continuous dividend yield |

---

## Quick start pro nový měsíc

1. **Fetch:** `python options_fetcher_final.py` + `python price_fetcher.py`
2. **Rate:** Stáhnout z US Treasury → uložit jako `rates_YYYY_MM_DD.txt`
3. **Enhanced config:** Přidat blok do `rate_functioner_complete.py` → spustit
4. **Greek rename:** Přidat blok do `rename_to_greeks.py` → spustit
5. **R finále:** Přidat bloky do `data_processing.rmd` → spustit
6. Hotovo: `complete_dataset.csv` obsahuje i nový měsíc
