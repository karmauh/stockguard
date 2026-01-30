import pandas as pd
from typing import Tuple

def evaluate_market_condition(row: pd.Series) -> Tuple[str, str]:
    """
    Evaluates market condition for a single row of data.
    Returns (Sentiment, Action).
    Sentiment: BULLISH, BEARISH, NEUTRAL
    Action: BUY, SELL, HOLD
    """
    # 1. Gather Signals
    rsi = row.get('rsi', 50)
    macd = row.get('macd', 0) # MACD Histogram
    price = row.get('close', 0)
    ma_50 = row.get('ma_50', price)
    
    # 2. Determine Sentiment (Bullish/Bearish/Neutral)
    score = 0
    if price > ma_50: score += 1
    else: score -= 1
    
    if macd > 0: score += 1
    else: score -= 1
    
    if rsi > 50: score += 0.5
    elif rsi < 50: score -= 0.5
    
    if score > 1:
        sentiment = "BULLISH"
    elif score < -1:
        sentiment = "BEARISH"
    else:
        sentiment = "NEUTRAL"
        
    # 3. Determine Action (Buy/Sell/Hold) - Classic RSI Logic
    # Strict implementation as requested:
    # High RSI (>70) -> SELL
    # Low RSI (<30) -> BUY
    
    action = "HOLD"
    
    if rsi < 30:
        action = "BUY"
    elif rsi > 70:
        action = "SELL"
    else:
        action = "HOLD"

    return sentiment, action
