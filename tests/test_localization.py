from fastapi.testclient import TestClient
from api.main import app
import json
import sys

client = TestClient(app)

def test_localization():
    print("Testing Localization (PL)...")
    payload = {
        "ticker": "AAPL",
        "start_date": "2023-01-01",
        "end_date": "2023-02-01",
        "contamination": 0.05,
        "language": "pl"
    }
    
    res = client.post("/api/analyze", json=payload)
    if res.status_code != 200:
        print(f"Request failed: {res.text}")
        sys.exit(1)
        
    data = res.json()
    analysis = data['llm_analysis']
    sentiment = data['sentiment']
    action = data['action']
    
    print(f"Sentiment: {sentiment} | Action: {action}")
    print("Analysis Snippet:", analysis[:100])
    
    if "Werdykt" in analysis or "Rekomendacja" in analysis:
        print("[SUCCESS] Found Polish keywords.")
    else:
        print("[FAILED] Polish keywords missing.")

    # Check for action column in data
    first_point = data['data'][0]
    if 'action' in first_point:
        print(f"[SUCCESS] Action field present in data points: {first_point['action']}")
    else:
        print("[FAILED] Action field missing in data points")

if __name__ == "__main__":
    test_localization()
