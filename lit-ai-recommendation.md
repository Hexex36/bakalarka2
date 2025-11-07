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

---

## IV. Doporučení z AI (Doplňková literatura)

Tato sekce obsahuje doplňkovou literaturu doporučenou umělou inteligencí na základě dotazů na klíčová témata z osnovy práce.

### 1. Sémantická a sentimentová analýza

*   **Knihy:**
    *   **Liu, Bing.** *Sentiment Analysis: Mining Opinions, Sentiments, and Emotions*. Cambridge University Press. (Považováno za jednu ze základních knih o sentimentální analýze).
    *   **Jurafsky, D., & Martin, J. H.** *Speech and Language Processing*. Prentice Hall. (Základní kniha v oboru zpracování přirozeného jazyka, pokrývá sémantiku i sentiment).
    *   **Goddard, Cliff.** *Semantic Analysis: A Practical Introduction*. Oxford University Press.

*   **Akademické žurnály a konference (pro nejnovější výzkum):**
    *   **Žurnály:** *Journal of Semantics*, *Computational Linguistics* (MIT Press).
    *   **Klíčové konference:** *ACL (Annual Meeting of the Association for Computational Linguistics)*, *EMNLP (Conference on Empirical Methods in Natural Language Processing)*. Sborníky jsou obvykle volně dostupné online.

### 2. Vývoj softwaru (Metodiky)

*   **Knihy (Základy softwarového inženýrství):**
    *   **Pressman, Roger S., & Maxim, Bruce R.** *Software Engineering: A Practitioner's Approach*. McGraw-Hill Education. (Komplexní "bible" softwarového inženýrství).
    *   **Sommerville, Ian.** *Software Engineering*. Pearson. (Další klíčová a komplexní učebnice oboru).
    *   **Brooks Jr., Frederick P.** *The Mythical Man-Month: Essays on Software Engineering*. Addison-Wesley Professional. (Klasické eseje o řízení softwarových projektů).

*   **Knihy (Principy a "řemeslo"):**
    *   **Martin, Robert C. (Uncle Bob).** *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.
    *   **Fowler, Martin.** *Refactoring: Improving the Design of Existing Code*. Addison-Wesley Professional.

*   **Akademické žurnály:**
    *   *IEEE Transactions on Software Engineering* (TSE)
    *   *ACM Transactions on Software Engineering and Methodology* (TOSEM)

### 3. Agilní přístup vs. Vodopádový model

Pro toto téma je nejlepší čerpat z akademických článků, které přímo srovnávají oba přístupy.

*   **Akademické články a studie:**
    *   *A Comparative Study of Agile and Waterfall Software Development Methodologies* (Razzak, M.A., et al., 2023).
    *   *Comparative Analysis of Waterfall and Agile Software Development Models: A Comprehensive Review* (IJSDR, 2024).
    *   *Agile vs. Waterfall: A Comprehensive Analysis of Methodologies for Effective Project Management* (IJNRD, 2025).
    *   *Effectiveness of Agile Compared to Waterfall Implementation Methods in IT Projects* (Dostupné přes Semantic Scholar).

*   **Případové studie (Case Studies):**
    *   *Comparative Analysis of Waterfall and Agile Methodologies in Microsoft* (IJEAIS, 2024).

*   **Klíčová témata v článcích:** Flexibilita vs. rigidita, role zpětné vazby, význam dokumentace, vhodnost pro různé typy projektů a hybridní přístupy. Pro plné texty hledejte názvy v databázích jako Google Scholar, IEEE Xplore, nebo ACM Digital Library.