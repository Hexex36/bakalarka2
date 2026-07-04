#!/usr/bin/env Rscript

library(readr)
library(dplyr)
library(knitr)
library(tidyr)

just_all <- read_csv("Data_fetch/complete_dataset.csv")

# ---- American summary ----
american_data <- just_all %>% filter(option_style == "American")

titul_summary_am <- american_data %>%
  group_by(ticker) %>%
  summarise(
    dividend_status = ifelse(max(q) > 0, "Dividendový", "Bezdividendový"),
    n_expirations = n_distinct(expiration),
    min_T = round(min(T), 3),
    max_T = round(max(T), 3),
    min_KS = round(min(pomer_K_S), 3),
    max_KS = round(max(pomer_K_S), 3),
    n_strikes = n_distinct(K),
    n_options = n(),
    .groups = "drop"
  ) %>%
  arrange(ticker)

# ---- European summary ----
european_data <- just_all %>% filter(option_style == "European")

titul_summary_eu <- european_data %>%
  group_by(ticker) %>%
  summarise(
    dividend_status = ifelse(max(q) > 0, "Dividendový", "Bezdividendový"),
    n_expirations = n_distinct(expiration),
    min_T = round(min(T), 3),
    max_T = round(max(T), 3),
    min_KS = round(min(pomer_K_S), 3),
    max_KS = round(max(pomer_K_S), 3),
    n_strikes = n_distinct(K),
    n_options = n(),
    .groups = "drop"
  ) %>%
  arrange(ticker)

# ---- Dividend split ----
dividend_split <- just_all %>%
  mutate(dividend_status = ifelse(q > 0, "Dividendové", "Bezdividendové")) %>%
  group_by(dividend_status, option_style, option_type) %>%
  summarise(pocet = n(), .groups = "drop") %>%
  pivot_wider(names_from = c(option_style, option_type), values_from = pocet, values_fill = 0)

# ---- Overview ----
n_dividend <- sum(titul_summary_am$dividend_status == "Dividendový") +
              sum(titul_summary_eu$dividend_status == "Dividendový")
n_nodividend <- sum(titul_summary_am$dividend_status == "Bezdividendový") +
                sum(titul_summary_eu$dividend_status == "Bezdividendový")

# ---- Write LaTeX output ----
sink("Psani/appendix_a.tex")

cat("\\section{Americké opce}\n\n")

kable(titul_summary_am,
      col.names = c("Titul", "Status", "# expirací", "Min T", "Max T", "Min K/S", "Max K/S", "# strike", "# opcí"),
      caption = "Sumarizace amerických opcí",
      format = "latex",
      booktabs = TRUE) %>%
  kableExtra::kable_styling(latex_options = "hold_position") %>%
  kableExtra::add_footnote("T je počítáno jako (dny do expirace + 1) / 365, tj. 0DTE opce mají T = 1/365 ≈ 0.003.")

cat("\n\n\\section{Evropské opce}\n\n")

kable(titul_summary_eu,
      col.names = c("Titul", "Status", "# expirací", "Min T", "Max T", "Min K/S", "Max K/S", "# strike", "# opcí"),
      caption = "Sumarizace evropských opcí",
      format = "latex",
      booktabs = TRUE) %>%
  kableExtra::kable_styling(latex_options = "hold_position") %>%
  kableExtra::add_footnote("T je počítáno jako (dny do expirace + 1) / 365, tj. 0DTE opce mají T = 1/365 ≈ 0.003.")

cat("\n\n\\section{Dividendové vs bezdividendové opce}\n\n")

kable(dividend_split,
      col.names = c("Status", "American Call", "American Put", "European Call", "European Put"),
      caption = "Počet opcí podle dividendového statusu a typu",
      format = "latex",
      booktabs = TRUE) %>%
  kableExtra::kable_styling(latex_options = "hold_position")

cat("\n\n\\section{Celkový přehled}\n\n")
cat("Celkový počet opcí:", nrow(just_all), "\\par\n")
cat("Počet titulů:", n_distinct(just_all$ticker), "\\par\n")
cat("Dividendové tituly:", n_dividend, "\\par\n")
cat("Bezdividendové tituly:", n_nodividend, "\\par\n")
cat("Rozsah T:", min(just_all$T), "až", max(just_all$T), "\\par\n")
cat("Rozsah strike cen:", min(just_all$K), "až", max(just_all$K), "\\par\n")

sink()
