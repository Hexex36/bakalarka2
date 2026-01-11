# Název práce

**Česky:** Modelování a oceňování finančních opcí pomocí diskrétních modelů
**Anglicky:** Modeling and Valuation of Financial Options using Discrete-Time Models

---

## Cíl práce

Cílem této bakalářské práce je vytvořit, implementovat a komplexně porovnat modely pro oceňování finančních opcí.

**Hlavní cíle:**
1.  Detailně popsat teoretické principy oceňování opcí, se zaměřením na Black-Scholesův model jako zástupce modelů ve spojitém čase a binomický model jako zástupce modelů v diskrétním čase (Markovských modelů).
2.  Vytvořit softwarovou implementaci obou modelů schopnou ocenit vanilkové (evropské i americké) a vybrané exotické opce.
3.  Provést komparativní analýzu obou modelů, zhodnotit jejich přesnost, rychlost a flexibilitu při oceňování různých typů opcí, s důrazem na rozdíly v oceňování vanilkových a exotických opcí.
4.  Prozkoumat oceňování opcí na akcie s různorodými charakteristikami podkladových aktiv.

**Vedlejší cíle:**
*   Porovnat ceny vypočtené modely s reálnými tržními daty vybraných akciových opcí.
*   Vytvořit vizualizace, které ilustrují fungování modelů (např. binomický strom) a srovnání výsledků.
*   Diskutovat omezení použitých modelů a navrhnout možná rozšíření.

---

## Osnova práce

**1. Úvod**
    *   1.1. Motivace a uvedení do problematiky finančních derivátů a opcí.
    *   1.2. Formulace cílů práce.
    *   1.3. Přehled struktury dokumentu.

**2. Teoretické základy oceňování opcí a stochastických procesů**
    *   2.1. Finanční opce
        *   2.1.1. Definice a základní pojmy (podkladové aktivum, strike cena, expirace).
        *   2.1.2. Typologie opcí (call vs. put).
        *   2.1.3. Vanilkové opce: Evropský vs. Americký styl.
        *   2.1.4. Krátký přehled exotických opcí.
    *   2.2. Základní principy oceňování
        *   2.2.1. Princip ne-arbitráže a replikační portfolio.
        *   2.2.2. Koncept risk-neutrálního oceňování.
    *   2.3. Modely ve spojitém čase: Black-Scholesův model
        *   2.3.1. Geometrický Brownův pohyb jako model ceny akcie.
        *   2.3.2. Předpoklady modelu (konstantní volatilita, bezriziková úroková míra atd.).
        *   2.3.3. Black-Scholesova parciální diferenciální rovnice a její analytické řešení.
        *   2.3.4. Parametry citlivosti ("The Greeks": Delta, Gamma, Vega, Theta).
        *   2.3.5. Limity a kritika Black-Scholesova modelu.
    *   2.4. Modely v diskrétním čase: Markovské modely
        *   2.4.1. Úvod do Markovských řetězců v diskrétním čase.
        *   2.4.2. Binomický model (Cox-Ross-Rubinstein) jako aplikace Markovského řetězce.
        *   2.4.3. Konstrukce binomického stromu a výpočet risk-neutrálních pravděpodobností.
        *   2.4.4. Oceňování evropských a amerických opcí pomocí zpětné indukce.
        *   2.4.5. Konvergence binomického modelu k Black-Scholesovu modelu.

**3. Implementace a experimentální design**
    *   3.1. Zdroje dat a jejich příprava
        *   3.1.1. Sběr tržních dat (historické ceny akcií, opční řetězce, bezriziková úroková míra).
        *   3.1.2. Výpočet klíčových parametrů: historická vs. implikovaná volatilita.
    *   3.2. Architektura softwarového řešení
        *   3.2.1. Popis použitých technologií (např. Python, NumPy, Pandas, Scipy).
        *   3.2.2. Návrh struktury kódu (objektové třídy pro opce, modely, atd.).
    *   3.3. Implementace oceňovacích modelů
        *   3.3.1. Funkce pro Black-Scholesův model.
        *   3.3.2. Implementace binomického modelu s podporou pro evropské i americké opce.
    *   3.4. Metodika testování a srovnání
        *   3.4.1. Definice testovacích scénářů pro různé typy opcí.
        *   3.4.2. Kritéria pro srovnání: přesnost ceny, rychlost výpočtu.

**4. Prezentace a zhodnocení výsledků**
    *   4.1. Validace modelů: Srovnání binomického modelu s Black-Scholes pro evropské opce.
        *   *Analýza konvergence a výpočetní náročnosti.*
    *   4.2. Komparativní analýza: Oceňování amerických opcí.
        *   *Demonstrace prémie za předčasné uplatnění.*
    *   4.3. Srovnání modelových cen s reálnými tržními daty.
        *   *Analýza odchylek a diskuze možných příčin (transakční náklady, nekonstantní volatilita).*
    *   4.4. Vizualizace výsledků
        *   *Grafy srovnání cen, vizualizace binomického stromu, povrchy implikované volatility.*

**5. Závěr**
    *   5.1. Shrnutí dosažených výsledků a naplnění cílů práce.
    *   5.2. Diskuze limitací provedené analýzy a použitých modelů.
    *   5.3. Návrhy na budoucí práci a možná rozšíření (např. trinomiální modely, Monte Carlo simulace, modely se stochastickou volatilitou).

---
**Seznam literatury**

**Seznam příloh**
