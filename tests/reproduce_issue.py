from fastapi.testclient import TestClient
from api.main import app
import json
import sys

client = TestClient(app)

def reproduce_error():
    print("reproducing error with short date range...")
    payload = {
        "ticker": "AAPL",
        "start_date": "2025-01-01",
        "end_date": "2025-01-31",
        "contamination": 0.05
    }
    res = client.post("/api/analyze", json=payload)
    print(f"Status Code: {res.status_code}")
    if res.status_code != 200:
        print(f"Response: {res.text}")

if __name__ == "__main__":
    reproduce_error()
