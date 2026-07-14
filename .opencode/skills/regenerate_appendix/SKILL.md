---
name: regen_appendix
description: Regenrate the appendix section of the main file.
---

# Příloha A – Sumarizace titulů

Pro přidání přílohy A do `Psani/bakalarka2.tex` je potřeba provést následující kroky:

## 1. Vygenerovat LaTeX tabulky

```bash
Rscript Psani/render_appendix_a.R
```

Toto vytvoří soubor `Psani/appendix_a.tex` s čistým LaTeX obsahem (žádná preambule).

## 2. Zkompilovat bakalářku

```bash
lualatex Psani/bakalarka2.tex
biber Psani/bakalarka2          # pokud je potřeba aktualizovat citace
lualatex Psani/bakalarka2.tex   # znovu pro reference
```

Nebo jednoduše přes vimtex (`:ll`).

## Co už je hotovo

- `Psani/render_appendix_a.R` – skript, který generuje tabulky
- `Psani/bakalarka2.tex` – v preambuli přidáno `\usepackage{float}` (ř. 14)
- `Psani/bakalarka2.tex` – na konci před `\end{document}` přidán appendix (ř. 1619–1621):
  ```latex
  \appendix
  \chapter{Sumarizace titulů použitých při případových analýzách}
  \input{appendix_a.tex}
  ```

## Kdy znovu spouštět `render_appendix_a.R`

- Pokud se změní `ticker_summary.rmd` (nové výpočty, sloupce, …)
- Pokud se změní `Data_fetch/complete_dataset.csv` (nová data)

Obojí se projeví až po opětovném spuštění R skriptu a následné kompilaci LaTeXu.
