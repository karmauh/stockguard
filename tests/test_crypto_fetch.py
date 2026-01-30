import yfinance as yf

def test_crypto():
    tickers = ["BTC-USD", "ETH-USD", "SOL-USD", "BTC-USDT"]
    for t in tickers:
        print(f"Fetching {t}...")
        df = yf.download(t, period="1mo", progress=False)
        if not df.empty:
            print(f"[SUCCESS] {t}: {len(df)} rows")
        else:
            print(f"[FAILED] {t}: No data")

if __name__ == "__main__":
    test_crypto()
