# 🛡️ StockGuard AI

**AI-Powered Stock Anomaly Detection & Analysis**

StockGuard AI is a sophisticated web application designed to help investors identify market anomalies, analyze technical trends, and receive AI-generated insights for both Stocks and Cryptocurrencies.

## 🚀 Features

- **Multi-Market Support**: Analyze **Stocks** (e.g., AAPL, NVDA) and **Cryptocurrencies** (e.g., BTC, ETH) seamlessly.
- **Anomaly Detection**: Uses unsupervised machine learning (**Isolation Forest**) to detect unusual price movements and volume spikes.
- **Technical Analysis**: Automatically calculates key indicators:
  - **Trend**: Moving Averages (50/200), ADX, Bollinger Bands, MACD.
  - **Momentum**: RSI, Stochastic Oscillator.
  - **Volume**: On-Balance Volume (OBV), Volume Spikes.
- **Algorithmic Signals**:
  - **Buy/Sell/Hold** recommendations based on technical strategy (e.g., RSI Classic Oversold/Overbought).
  - **Bullish/Bearish** market sentiment assessment.
  - Visualized on charts with Green (Buy) and Red (Sell) markers.
- **AI Analyst**: Generates natural language interpretations of the market context and anomalies.
  - _Note: Currently runs with a robust Mock LLM that simulates analysis logic logic. Pluggable architecture allows easy connection to OpenAI/Anthropic._
- **Localization**: Fully localized interface and reports in **English** and **Polish**.
- **PDF Reports**: Generate and download professional PDF reports of the analysis.

## 🛠️ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python web API.
- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive data dashboard.
- **ML & Data**: `scikit-learn` (Isolation Forest), `pandas`, `numpy`, `yfinance`, `ta` (Technical Analysis library).
- **Visualization**: `plotly`.

## 📦 Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/karmauh/stockguard.git
    cd stockguard
    ```

2.  **Create a virtual environment**:

    ```bash
    # Windows
    py -m venv .venv
    \.venv\Scripts\activate

    # Mac/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Environment Setup**:
    Copy the example environment file (optional for now, but good practice):
    ```bash
    cp .env.example .env
    ```

## 🚀 Usage

To run the application, you need to start **two separate terminals**: one for the Backend API and one for the Frontend UI.

**Terminal 1: Backend API**

```bash
uvicorn api.main:app --reload
```

_The API will start at `http://localhost:8000`_

**Terminal 2: Frontend Dashboard**

```bash
streamlit run ui/app.py
```

_The dashboard will open automatically in your browser (usually `http://localhost:8501`)._

## 🧪 Testing

The repository includes a suite of test scripts in the `tests/` directory to verify functionality:

- `test_system.py`: End-to-end test of the Analysis and Report API endpoints.
- `test_localization.py`: Verifies that language selection works correctly.
- `test_crypto_fetch.py`: Verifies connectivity to crypto data sources.

To run a test (ensure server is running or use the `TestClient` scripts):

```bash
python tests/test_system.py
```

## 📄 License

MIT License. See `LICENSE` file for details.
