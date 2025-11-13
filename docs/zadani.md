# Návrh zadání závěrečné práce (Bakalářská práce)

## Název tématu v češtině:
**Modelování cen finančních aktiv diskrétními Markovovými řetězci a jejich aplikace v opčních strategiích**

## Název tématu v angličtině:
**Modeling of Financial Asset Prices with Discrete-Time Markov Chains and Their Application in Option Strategies**

---

### Anotace tématu

#### Motivace tématu:
Pro kvantitativní analytiky a portfoliové manažery je predikce cen finančních aktiv, jako jsou akcie, komodity nebo kryptoměny, klíčová. Diskrétní Markovovy řetězce poskytují robustní matematický model pro simulaci budoucího cenového pohybu. Avšak skutečná hodnota takového modelu spočívá v jeho praktické aplikaci. Práce se zaměří na přeměnu pravděpodobnostního výstupu z Markova modelu na **konkrétní obchodní strategie**, primárně s využitím **opcí**, které jsou ideální pro monetizaci a zajištění rizik spojených s očekávanými cenovými pohyby (např. *Bull/Bear Spread*). Cílem je propojit stochastické modelování s reálným finančním inženýrstvím.

#### Cíl práce:
Cílem této bakalářské práce je **navrhnout, implementovat a kriticky zhodnotit diskrétní Markovův řetězec** pro modelování budoucího vývoje cen vybraných finančních aktiv. Hlavním cílem je na základě výsledků simulace **navrhnout a otestovat konkrétní obchodní strategie (včetně opčních strategií)**, které využívají pravděpodobnostně definovaný očekávaný pohyb aktiv.

#### Cíle práce (Podrobný rozpis):
* **Rešerše metodiky:** Přehled teoretických základů Markovových procesů a opčních strategií (včetně základního ocenění opcí a Greeků).
* **Sběr a analýza dat:** Získání a zpracování historických dat o cenách vybraných aktiv (akcie, komodita, kryptoměna).
* **Definice stavů a přechodů:** Definice **diskrétních cenových stavů** a konstrukce **matice přechodových pravděpodobností**.
* **Návrh a implementace modelu:** Implementace Markova modelu a provedení **Monte Carlo simulace** budoucího vývoje cen pro zvolené časové horizonty.
* **Tvorba obchodních strategií:** **Návrh sady konkrétních strategií** (včetně minimálně dvou **opčních strategií**), které jsou postaveny na výsledcích Markova modelu.
* **Simulace ziskovosti:** **Testování výkonnosti** navržených obchodních strategií pomocí backtestingu na historických datech.
* **Zhodnocení a doporučení:** Kritické vyhodnocení přesnosti modelu a porovnání ziskovosti / rizika navržených strategií.

#### Výstupy práce:
Výstupem práce bude **funkční stochastický model pro simulaci cen**, a co je klíčové, **sada konkrétních obchodních a opčních strategií** odvozených z pravděpodobnostního výstupu modelu. Klíčovým výstupem je **analýza finančního dopadu** navržených strategií, včetně metrik rizika a výnosu (např. Sharpe Ratio).

---

### Osnova:

1.  **Úvod**
    * Motivace a předmět práce.
    * Formulace cílů.
    * Struktura práce.
2.  **Přehled současného stavu problematiky**
    * Rešeršní část zaměřená na stochastické modely ve finančnictví (Markovovy řetězce, diskretizace cen).
    * Přehled základních a pokročilých **opčních strategií**.
    * Analýza trendů v aplikaci pravděpodobnostních modelů pro automatizované obchodování.
3.  **Teoretická část – Modelování a oceňování**
    * **Diskrétní Markovovy řetězce:** Definice, matice přechodových pravděpodobností, limitní rozdělení.
    * **Oceňování opcí a Greekové:** Základy modelu pro kontext a řízení rizika.
    * **Propojení modelu a strategie:** Metodika převodu pravděpodobnostních výstupů na obchodní signály.
4.  **Praktická část – Aplikace, simulace a obchodní strategie**
    * Příprava dat a **definice cenových stavů** pro vybraná aktiva.
    * **Konstrukce a analýza matice přechodových pravděpodobností**.
    * **Simulace (Monte Carlo) budoucího cenového vývoje**.
    * **Návrh obchodních strategií:** Standardní strategie a **Opční strategie** určené k maximalizaci zisku/minimalizaci rizika.
    * **Backtesting a zhodnocení výkonnosti** navržených strategií.
5.  **Závěr**
    * Rekapitulace motivace a cíle práce.
    * Dosažené výsledky ve vztahu k formulovaným cílům.
    * Objektivní přínosy práce a **doporučení pro implementaci obchodních algoritmů**.
    * Možnosti dalšího výzkumu a rozvoje modelu.

---

### Literatura:
*(Upozornění: Doplňte relevantní zdroje, zejména ty týkající se stochastického modelování, oceňování opcí a obchodních strategií.)*

* Ross, S. M. (2014). *Introduction to Probability Models* (11th ed.).
* Taylor, H. M., & Karlin, S. (1998). *An Introduction to Stochastic Modeling* (3rd ed.).
* Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.). Pearson Education.
* **(Zdroje k pokročilým obchodním a opčním strategiím a finančnímu inženýrství.)**
* Dokumentace k softwarovým nástrojům (Python/R knihovny pro statistiku a finance).
