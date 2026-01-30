from fastapi import APIRouter, HTTPException
from api.schemas import AnalysisRequest, AnalysisResponse
from core.data_loader import fetch_data
from core.features import add_technical_indicators
from core.anomaly import detect_anomalies
from core.llm import MockLLM
from core.llm import MockLLM
import json
import pandas as pd

router = APIRouter()
llm = MockLLM()

from core.utils import get_lookback_date

@router.post("/analyze", response_model=AnalysisResponse)
def analyze_stock(request: AnalysisRequest):
    # 1. Fetch Data with Lookback Buffer (365 days for MA200 stability)
    buffered_start_date = get_lookback_date(request.start_date, 365)
    
    df = fetch_data(request.ticker, buffered_start_date, request.end_date)
    if df is None:
        raise HTTPException(status_code=404, detail="Stock data not found")
    
    # 2. Add Features
    try:
        df = add_technical_indicators(df)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature engineering failed: {str(e)}")
        
    if df.empty:
        raise HTTPException(status_code=422, detail="Starting data was insufficient to generate technical indicators (requires > 200 days of history).")
        
    # 3. Detect Anomalies
    try:
        df = detect_anomalies(df, contamination=request.contamination)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection failed: {str(e)}")
    
    # 4. Filter Anomalies for LLM
    # FIRST, filter data back to the requested user range
    # Ensure date column is datetime for comparison
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        
    mask = (df['date'] >= pd.to_datetime(request.start_date)) & (df['date'] <= pd.to_datetime(request.end_date))
    df_filtered = df.loc[mask].copy()
    
    if df_filtered.empty:
         # Fallback if filtering removed everything (e.g. data ends before start date)
         raise HTTPException(status_code=422, detail="No data available for the requested specific period (after processing).")

    # Use filtered data for LLM and Response
    anomalies = df_filtered[df_filtered['anomaly'] == -1]
    
    # 5. Generate Analysis
    # Get latest data point for context
    latest_data = df_filtered.iloc[-1]
    
    llm_result = llm.generate_analysis(request.ticker, anomalies, latest_data, language=request.language)
    
    # 6. Prepare Response
    # Convert date to string for JSON serialization
    df_filtered['date'] = df_filtered['date'].astype(str)
    
    # Convert dataframe to list of dicts
    data_points = df_filtered.to_dict(orient='records')
    
    return AnalysisResponse(
        ticker=request.ticker,
        data=data_points,
        anomalies_count=len(anomalies),
        llm_analysis=llm_result['text'],
        sentiment=llm_result['sentiment'],
        action=llm_result['action']
    )
