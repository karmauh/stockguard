import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    """
    Detects anomalies in stock data using Isolation Forest.
    
    Args:
        df: DataFrame with features.
        contamination: The proportion of outliers in the data set.
        
    Returns:
        DataFrame with an 'anomaly' column (-1 for anomaly, 1 for normal).
    """
    # Select features for the model
    # We exclude Date and OHLC raw values usually, focusing on derived features (returns, indicators)
    feature_cols = [
        'returns', 'log_returns', 'volatility_14', 
        'rsi', 'macd', 
        'vol_spike',
        'atr', 'adx', 'stoch_k', 'dist_ma_50', 'dist_ma_200'
    ]
    
    # Filter only columns that exist
    features_to_use = [c for c in feature_cols if c in df.columns]
    
    if not features_to_use:
        print("No features available for anomaly detection.")
        return df
    
    X = df[features_to_use]
    
    # Check if we have enough data
    if len(X) < 50:
        print("Not enough data points for reliable anomaly detection.")
        df['anomaly'] = 1
        df['anomaly_score'] = 0.0
        return df

    # Initialize and fit
    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    df['anomaly'] = iso_forest.fit_predict(X)
    df['anomaly_score'] = iso_forest.decision_function(X) # lower is more anomalous
    
    # Map -1 to True (Anomaly) and 1 to False (Normal) for easier handling if preferred
    # But usually keeping -1/1 is standard Scikit-learn
    
    return df
