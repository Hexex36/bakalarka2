# Option Fetcher
- V podstatě kompletní, nevím jestli má smysl ukládat všechno though

# Sentiment Fetcher
- [ ] Základní model
    - [ ] Zdroje analýzy (pro zákl. model jenom jeden)
        * *Finnhub?*
        * *EODHD?*
        - [ ] Seber data, získej headlineu
    - [ ] FinBERT analýza
        - [ ] Uveď zdroje
        - [ ] Vytvoř model a pipeline
        - [ ] Zaveď do toho ty headlines
    - [ ] Upload do databáze
        - [ ] Vytvoř tabulku

- [ ] Advanced model
    - Zdroje:
        - Finnhub a EODHD
        - Reddit (r/wallstreetbets?)
-----
- Stocks netřeba hledat, jsou dostupné
- V zaslaných souborech jsou Yahoo Finance web scrapery, které by měly rovnou brát dle tickerů
    - Stránky YFinance pro dané tickery obsahují zprávy
- Stáhni si data do databáze
- Stáhnout články k akciím
- Jdi rok nebo víc zpátky
- Stáhni info pro celý trh a specifický tickery
- Skript na webscraping je na Mattermostu, něco dalšího na OwnCloud
- Pomocí "Inspect Element" lze najít exposed YFinance endpointy, posílat requesty a dostat jsony
