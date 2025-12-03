CREATE TABLE IF NOT EXISTS "calls" (
  id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "ticker" VARCHAR(16),
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
  "ticker" VARCHAR(16),
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
  "id" INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  "title" TEXT NOT NULL,
  "url" TEXT UNIQUE NOT NULL,
  "source" TEXT NOT NULL, -- Maybe have a M:N relationship to be more sure?
  "summary" TEXT,
  "ticker" VARCHAR(16) NOT NULL,
  "sentiment" DOUBLE PRECISION NOT NULL,
  "date" TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Recommended Indexes:

-- Index for quick lookups by ticker symbol
CREATE INDEX IF NOT EXISTS idx_sentiment_ticker ON sentiment_pieces(ticker);

-- Index for filtering/sorting by date
CREATE INDEX IF NOT EXISTS idx_sentiment_date ON sentiment_pieces(date);

-- A composite index for finding sentiment for a specific ticker over time.
CREATE INDEX IF NOT EXISTS idx_sentiment_ticker_date ON sentiment_pieces(ticker, date);

