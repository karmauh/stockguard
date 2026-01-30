from pydantic import BaseModel
from typing import List, Optional

class AnalysisRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    contamination: float = 0.05
    language: str = 'pl'

class StockDataPoint(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    rsi: Optional[float] = None
    vol_spike: Optional[float] = None
    macd: Optional[float] = None
    volatility_14: Optional[float] = None
    atr: Optional[float] = None
    adx: Optional[float] = None
    stoch_k: Optional[float] = None
    dist_ma_50: Optional[float] = None
    dist_ma_200: Optional[float] = None
    obv: Optional[float] = None
    action: Optional[str] = None
    anomaly: int  # -1 or 1

class AnalysisResponse(BaseModel):
    ticker: str
    data: List[StockDataPoint]
    anomalies_count: int
    llm_analysis: str
    sentiment: str
    action: str

class ReportRequest(BaseModel):
    ticker: str
    analysis: str
    anomalies_json: str # JSON string or we can accept list of objects, but simplified for PDF generation
