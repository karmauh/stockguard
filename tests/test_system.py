from fastapi.testclient import TestClient
from api.main import app
import json
import sys
import os

client = TestClient(app)

def test_pipeline():
    # 1. Test Analysis
    print("Testing Analysis Endpoint...")
    # Use a longer date range to ensure we have enough data for 200-day MA + drops
    payload = {
        "ticker": "AAPL",
        "start_date": "2022-01-01",
        "end_date": "2023-01-01",
        "contamination": 0.05
    }
    try:
        res = client.post("/api/analyze", json=payload)
        if res.status_code != 200:
            print(f"Analysis failed: {res.text}")
            sys.exit(1)
            
        data = res.json()
        points = data['data']
        print(f"Analysis Success! Data points: {len(points)}")
        print(f"Sentiment: {data.get('sentiment')} | Action: {data.get('action')}")
        
        if len(points) > 0:
            first_point = points[0]
            print("Verifying new indicators in response...")
            required_fields = ['atr', 'adx', 'stoch_k', 'dist_ma_50', 'obv']
            for field in required_fields:
                if field in first_point and first_point[field] is not None:
                    print(f"  [x] {field} present: {first_point[field]:.4f}")
                else:
                    print(f"  [ ] {field} MISSING or None")
                    # It might be None if nan, but we dropped nans.
        
        # 2. Test Report
        print("Testing Report Endpoint...")
        anomalies_list = [d for d in points if d['anomaly'] == -1]
        
        report_payload = {
            "ticker": "AAPL",
            "analysis": data['llm_analysis'],
            "anomalies_json": json.dumps(anomalies_list)
        }
        
        rep_res = client.post("/api/report", json=report_payload)
        
        if rep_res.status_code != 200:
             print(f"Report failed: {rep_res.text}")
             sys.exit(1)
             
        if rep_res.headers['content-type'] == 'application/pdf':
            print("Report Generation Success! PDF received.")
        else:
            print("Report generation failed: Content type mismatch.")
            
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_pipeline()
