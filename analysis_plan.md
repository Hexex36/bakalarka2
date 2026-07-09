# Tabulka s daty

- Parametry: S, K, r, sigma, T, q, am/eu, call/put, teoretprice, model, ticker, true price, (teor price - true price)/true price

# Deskriptivní statistika

Skript: `Misc_scripts/descriptive_stats.R`
Data: `Misc_scripts/analysis_data.csv`

## 0 – Global overview
- `describe()` nebo `summary()` všech sloupců v datasetu (NA counts, min/max, mean, unique values)

## 1 – Coverage
- Počet opcí na kategorii (am_eu × call_put)
- Počet opcí na ticker × kategorie
- Sloupcový graf: počet opcí na ticker
- `describe()` per ticker – přehled cenového rozpětí a parametrů (S, K, sigma, T, q) pro každý titul

## 2 – Distribuce vstupních parametrů
- Summary tabulka (mean, sd, min, max, median) S, K, r, sigma, T, q grouped by am_eu, call_put
- Histogramy sigma, T, r (faceted)

## 3 – Moneyness & time profily
- Podíl OTM/ATM/ITM a Short/Medium/Long na kategorii (tabulka + bar chart)

## 4 – Ceny: trh vs model
- Summary tabulka true_price a teor_price grouped by am_eu, call_put, model
- Boxplot true_price vs teor_price per model

## 5 – Relativní chyba
- Summary tabulka rel_error (mean, median, sd, Q1, Q3, p5, p95) grouped by am_eu, call_put, model
- Density plot rel_error colored by model, faceted by category
- Heatmapa průměrného rel_error v gridu moneyness × T

## 6 – Převzato z results.Rmd
- Scatter plot true_price vs teor_price (facet category ~ model)
- Error summary table: MAE, RMSE, Bias per category a model

# Regrese
