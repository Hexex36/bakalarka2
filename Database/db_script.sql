CREATE TABLE IF NOT EXISTS "calls" (
  id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "ticker" VARCHAR(4),
  "contractSymbol" TEXT,
  "lastTradeDate" TIMESTAMP WITH TIME ZONE,
  "strike" DOUBLE PRECISION,
  "lastPrice" DOUBLE PRECISION,
  "bid" DOUBLE PRECISION,
  "ask" DOUBLE PRECISION,
  "change" DOUBLE PRECISION,
  "percentChange" DOUBLE PRECISION,
  "volume" DOUBLE PRECISION,
  "openInterest" DOUBLE PRECISION,
  "impliedVolatility" DOUBLE PRECISION,
  "inTheMoney" BOOLEAN,
  "contractSize" TEXT,
  "currency" TEXT,
  "expirationDate" TIMESTAMP,
  "uploadTime" TIMESTAMP
);

-- Recommended Indexes:

-- Index for quick lookups by ticker symbol
CREATE INDEX IF NOT EXISTS idx_calls_ticker ON calls(ticker);

-- A composite index for the most common query pattern: finding contracts
-- for a specific ticker, often sorted or filtered by expiration date.
CREATE INDEX IF NOT EXISTS idx_calls_ticker_expirationDate ON calls(ticker, "expirationDate");

-- Index for looking up a specific contract by its full symbol.
CREATE INDEX IF NOT EXISTS idx_calls_contractSymbol ON calls("contractSymbol");

CREATE INDEX IF NOT EXISTS idx_calls_itm ON calls USING HASH ("inTheMoney");

CREATE TABLE IF NOT EXISTS "puts" (
  id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "ticker" VARCHAR(4),
  "contractSymbol" TEXT,
  "lastTradeDate" TIMESTAMP WITH TIME ZONE,
  "strike" DOUBLE PRECISION,
  "lastPrice" DOUBLE PRECISION,
  "bid" DOUBLE PRECISION,
  "ask" DOUBLE PRECISION,
  "change" DOUBLE PRECISION,
  "percentChange" DOUBLE PRECISION,
  "volume" DOUBLE PRECISION,
  "openInterest" DOUBLE PRECISION,
  "impliedVolatility" DOUBLE PRECISION,
  "inTheMoney" BOOLEAN,
  "contractSize" TEXT,
  "currency" TEXT,
  "expirationDate" TIMESTAMP,
  "uploadTime" TIMESTAMP
);

-- Recommended Indexes:

-- Index for quick lookups by ticker symbol
CREATE INDEX IF NOT EXISTS idx_puts_ticker ON puts(ticker);

-- A composite index for the most common query pattern: finding contracts
-- for a specific ticker, often sorted or filtered by expiration date.
CREATE INDEX IF NOT EXISTS idx_puts_ticker_expirationDate ON puts(ticker, "expirationDate");

-- Index for looking up a specific contract by its full symbol.
CREATE INDEX IF NOT EXISTS idx_puts_contractSymbol ON puts("contractSymbol");

CREATE INDEX IF NOT EXISTS idx_puts_itm ON puts USING HASH ("inTheMoney");

CREATE TABLE IF NOT EXISTS "sentiment_pieces" (

)
