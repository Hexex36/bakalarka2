library(readr)
library(dplyr)
library(tidyr)

csv_files <- c(
  "american_calls" = "calculated_prices/american_calls.csv",
  "american_puts"  = "calculated_prices/american_puts.csv",
  "european_calls" = "calculated_prices/european_calls.csv",
  "european_puts"  = "calculated_prices/european_puts.csv"
)

parse_category <- function(name) {
  parts <- strsplit(name, "_")[[1]]
  list(am_eu = parts[1], call_put = parts[2])
}

all_data <- bind_rows(lapply(names(csv_files), function(nm) {
  df <- read_csv(csv_files[nm])
  parsed <- parse_category(nm)
  df$am_eu <- parsed$am_eu
  df$call_put <- parsed$call_put
  df
}))

long_data <- all_data %>%
  pivot_longer(
    cols = c(user_bs, user_crr, user_mc),
    names_to = "model",
    values_to = "teor_price"
  ) %>%
  mutate(
    model = recode(model,
      user_bs  = "bs",
      user_crr = "crr",
      user_mc  = "mc"
    ),
    rel_error = (teor_price - option_price) / option_price
  ) %>%
  select(ticker, S, K, r, sigma, T, q, am_eu, call_put,
         true_price = option_price, model, teor_price, rel_error)

write_csv(long_data, "Misc_scripts/analysis_data.csv")
