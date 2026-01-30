import pandas as pd
import numpy as np
import ta
from core.strategy import evaluate_market_condition

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds technical indicators to the DataFrame.
    Expected columns: 'close', 'high', 'low', 'volume'
    """
    df = df.copy()
    
    # ensure sorted by date
    # ensure sorted by date
    if 'date' in df.columns:
        df = df.sort_values(by='date')
        
    if len(df) < 50:
         # 50 is min for MA50, but let's say 30 for safety of other indicators
         # If < 50, MA50 will be all NaN, and dropna will kill it anyway.
         # But to avoid 'IndexError' in TA lib, we should stop early.
         raise ValueError(f"Insufficient data for technical analysis. Got {len(df)} rows, need at least 50.")
    
    # Clean data: drop any rows with NaN in critical columns before starting
    df.dropna(subset=['close', 'high', 'low', 'volume'], inplace=True)
    
    # 0. Basics
    df['returns'] = df['close'].pct_change()
    df['log_returns'] = np.log(df['close'] / df['close'].shift(1))
    
    # 1. Volatility (Rolling Std Dev)
    df['volatility_14'] = df['log_returns'].rolling(window=14).std()
    
    # 2. Moving Averages
    df['ma_50'] = ta.trend.sma_indicator(df['close'], window=50)
    df['ma_200'] = ta.trend.sma_indicator(df['close'], window=200)
    
    # Distance from MA (Price-to-trend relationship)
    df['dist_ma_50'] = (df['close'] - df['ma_50']) / df['ma_50']
    df['dist_ma_200'] = (df['close'] - df['ma_200']) / df['ma_200']

    # 3. RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    
    # 4. MACD
    df['macd'] = ta.trend.macd_diff(df['close']) # This is often the histogram
    # Or strict MACD line:
    # df['macd_line'] = ta.trend.macd(df['close'])
    # df['macd_signal'] = ta.trend.macd_signal(df['close'])
    
    # 5. Bollinger Bands
    indicator_bb = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    df['bb_mid'] = indicator_bb.bollinger_mavg()
    df['bb_upper'] = indicator_bb.bollinger_hband()
    df['bb_lower'] = indicator_bb.bollinger_lband()
    df['bb_width'] = indicator_bb.bollinger_wband()
    
    # 6. ATR (Average True Range) - Volatility
    df['atr'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
    
    # 7. ADX (Average Directional Index) - Trend Strength
    df['adx'] = ta.trend.adx(df['high'], df['low'], df['close'], window=14)
    
    # 8. Stochastic Oscillator - Momentum
    df['stoch_k'] = ta.momentum.stoch(df['high'], df['low'], df['close'], window=14, smooth_window=3)
    
    # 9. On-Balance Volume (OBV) - Volume Flow
    df['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
    
    # 10. Volume Spikes
    df['vol_ma_20'] = df['volume'].rolling(window=20).mean()
    df['vol_spike'] = df['volume'] / df['vol_ma_20']
    
    # Drop rows with NaN created by rolling windows to avoid issues in ML
    # Note: 200-day MA will cause first 200 rows to be dropped.
    df.dropna(inplace=True)
    
    # 11. Calculate Strategy Signals for the entire dataframe
    # We apply this AFTER dropna so we have valid indicators
    if not df.empty:
        # returns tuple (sentiment, action) -> expand to columns
        signals = df.apply(lambda row: evaluate_market_condition(row), axis=1)
        df['sentiment'] = [x[0] for x in signals]
        df['action'] = [x[1] for x in signals]

    # If cleaning results in empty df, outside caller should handle it.
    
    return df
