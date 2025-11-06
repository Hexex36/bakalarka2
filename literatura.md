Markovské řetezce:
- KOŘENÁŘ, Václav. Stochastické procesy. Vyd. 2. přeprac. Praha: Oeconomica, 2010. ISBN 978-80-245-1646-2.
- https://www.numberanalytics.com/blog/ultimate-guide-markov-chains-quantitative-methods
    - KENTON, Will. Understanding Markov Analysis: Simple Forecasting Method and Applications. Online. INVESTOPEDIA. Www.investopedia.com. 2025, 9. 11. 2025. Dostupné z: https://www.investopedia.com/terms/m/markov-analysis.asp. [cit. 2025-10-30].
- (?) SKALSKÁ, Hana. Stochastické modelování. Hradec Králové: Gaudeamus, 1998. ISBN 80-7041-039-6.

Opce a takové:
- https://skolainvestoru.cz/derivaty/
- ŠAFAŘÍK, Pavel. Denní obchodování na finančních trzích. 2. vydání (v Ekopressu 1.). Jesenice: Ekopress, 2019. ISBN 978-80-87865-56-9.

Samotné modelování:
- {Dokumentace Pythonu, NumPy a Matplotlib (možná SciPy?)}
    - PYTHON SOFTWARE FOUNDATION. Python 3.14.0 Documentation. Online. 30. 8. 2025. Dostupné z: https://docs.python.org/3/. [cit. 2025-10-30].

Všechno by mělo být nalezitelné buď na daném linku nebo v katalogu knihovny UJEP.

---
---

# Doporučená literatura pro Bakalářskou práci

Práce vyžaduje mezioborový přístup, proto je literatura rozdělena do tří hlavních sekcí: Teorie stochastického modelování, Kvantitativní finance a Opční strategie a Implementace a Data.

---

## I. Teorie stochastického modelování (Základ modelu)

Tyto zdroje jsou klíčové pro pochopení principů Markovových řetězců, které tvoří jádro modelu pro predikci pohybu aktiv.

* **Ross, S. M.** (*Introduction to Probability Models*, 11. vydání). Academic Press.
    * **Klíčové kapitoly:** Kapitoly o **diskrétních Markovových řetězcích (Discrete-Time Markov Chains)**, klasifikaci stavů, maticích přechodových pravděpodobností a limitním rozdělení.
* **Taylor, H. M., & Karlin, S.** (*An Introduction to Stochastic Modeling*, 3. vydání). Academic Press.
    * Užitečné pro hlubší matematické pochopení **stochastických procesů** a jejich použití v modelování reálných systémů.
* **Anděl, J.** (*Základy matematické statistiky* / *Matematika ve financích*).
    * Případně jiná relevantní **česká/slovenská učebnice pravděpodobnosti a statistiky** pro zajištění potřebné terminologie.

---

## II. Kvantitativní finance a Opční strategie (Aplikace)

Tyto knihy jsou nezbytné pro finanční inženýrství, oceňování opcí a odvození Greeků.

* **Hull, J. C.** (*Options, Futures, and Other Derivatives*, 10. vydání). Pearson Education.
    * **NEJDŮLEŽITĚJŠÍ ZDROJ:** Pokrývá **kompletní teorii derivátů**, oceňování opcí (**Black-Scholes-Mertonův model**), **řecká písmena (Greeks)**, a principy delta-neutrálního zajištění.
* **Neftci, S. N.** (*An Introduction to the Mathematics of Financial Derivatives*). Academic Press.
    * Poskytuje detailní **matematické odvození Black-Scholes PDR** a vysvětluje, jak jsou z ní odvozeny Greekové jako parciální derivace.
* **Natenberg, S.** (*Option Volatility and Pricing: A Trader's Guide to Strategy, Analysis, and Techniques*, 2. vydání). McGraw-Hill Education.
    * Vysoce **prakticky orientovaná** kniha zaměřená na **opční strategie** a jejich řízení pomocí Greeků a volatility. Klíčová pro návrh obchodních strategií v praktické části práce.
* **Cox, J. C., Ross, S. A., & Rubinstein, M.** (*Option Pricing: A Simplified Approach*). Journal of Financial Economics.
    * Klasický článek, který popisuje **Binomický model oceňování opcí**, který je často intuitivnější alternativou k BSM modelu a může být použit pro validaci výsledků.

---

## III. Implementace a Data (Praktická část)

Zdroje pro technické zpracování dat a programování modelu.

* **McKinney, W.** (*Python for Data Analysis*, 3. vydání). O'Reilly Media.
    * Učebnice knihovny **Pandas** v Pythonu, která je nezbytná pro efektivní práci s **časovými řadami** finančních dat (čištění, transformace a diskretizace).
* **Python/R Dokumentace knihoven:**
    * **NumPy** a **SciPy:** Pro práci s maticemi (přechodové pravděpodobnosti) a numerické simulace (Monte Carlo).
    * **Matplotlib / Seaborn:** Pro vizualizaci cenových řad, simulací a výsledků backtestingu.
* **Odborné články/Studie:**
    * Vyhledat aktuální **akademické články** (např. v databázích jako JSTOR, Scopus) specificky na téma **"Markov Chain application in quantitative finance"** nebo **"Using Monte Carlo simulation with Markov Chains for option strategies"** pro ověření metodiky.
