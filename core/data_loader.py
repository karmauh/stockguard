import yfinance as yf
import pandas as pd
from typing import Optional

def fetch_data(ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    Fetches historical stock data from Yahoo Finance.

    Args:
        ticker (str): The stock ticker symbol (e.g., "AAPL").
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: A DataFrame containing OHLCV data, or None if no data found.
    """
    try:
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if df.empty:
            print(f"No data found for {ticker}.")
            return None
            
        # Ensure flat index if multi-index is returned (common in recent yfinance versions)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # Reset index to make Date a column if it's the index
        df.reset_index(inplace=True)
        
        # Standardize column names
        df.columns = [c.lower() for c in df.columns]
        
        # Ensure we have required columns
        required_cols = {'date', 'open', 'high', 'low', 'close', 'volume'}
        if not required_cols.issubset(set(df.columns)):
             # Sometimes yfinance returns 'Adj Close', handle if needed or just minimal check
             pass
             
        print(f"Successfully fetched {len(df)} records.")
        return df

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

if __name__ == "__main__":
    # Simple test
    data = fetch_data("AAPL", "2023-01-01", "2023-12-31")
    if data is not None:
        print(data.head())
