import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
import json

# Configuration
API_URL = "http://localhost:8000/api"

st.set_page_config(page_title="StockGuard AI", layout="wide")

# Localization Dictionary
TRANSLATIONS = {
    'pl': {
        'page_title': "StockGuard AI",
        'title': "🛡️ StockGuard AI",
        'subtitle': "### Analiza i Wykrywanie Anomalii Giełdowych AI",
        'config': "Konfiguracja",
        'lang': "Język / Language",
        'market_type': "Rodzaj Rynku",
        'stock': "Akcje",
        'crypto': "Kryptowaluty",
        'ticker_stock': "Symbol Akcji",
        'ticker_crypto': "Symbol Krypto (np. BTC)",
        'start_date': "Data Początkowa",
        'end_date': "Data Końcowa",
        'sensitivity': "Czułość na Anomalie",
        'sensitivity_help': "Określa procent danych, które mają być uznane za anomalie. Wyższa wartość (np. 0.1) oznacza więcej wykrytych anomalii (bardziej czuły), niższa (np. 0.01) oznacza tylko najbardziej ekstremalne przypadki.",
        'analyze_btn': "Analizuj",
        'analysis_header': "Analiza dla",
        'sentiment': "Sentyment Rynkowy",
        'action': "Rekomendacja",
        'anomalies_count': "Liczba Anomalii",
        'tabs_price': "Cena i Wskaźniki Bazowe",
        'tabs_tech': "Momentum Techniczne",
        'llm_header': "🤖 Interpretacja Analityka AI",
        'anomalies_table': "Szczegóły Wykrytych Anomalii",
        'no_anomalies': "Nie wykryto anomalii.",
        'generate_pdf': "Generuj Raport PDF",
        'download_pdf': "Pobierz PDF",
        'error_api': "Błąd połączenia z API",
        'warning_nodata': "Brak danych dla wybranego okresu.",
        'info_start': "Wpisz symbol i kliknij 'Analizuj', aby rozpocząć."
    },
    'en': {
        'page_title': "StockGuard AI",
        'title': "🛡️ StockGuard AI",
        'subtitle': "### AI-Powered Stock Anomaly Detection & Analysis",
        'config': "Configuration",
        'lang': "Language",
        'market_type': "Market Type",
        'stock': "Stock",
        'crypto': "Crypto",
        'ticker_stock': "Stock Ticker",
        'ticker_crypto': "Crypto Symbol (e.g. BTC)",
        'start_date': "Start Date",
        'end_date': "End Date",
        'sensitivity': "Anomaly Sensitivity",
        'sensitivity_help': "Determines the percentage of data to be flagged as anomalies. Higher value (e.g., 0.1) means more anomalies detected (more sensitive), lower (e.g., 0.01) means only the most extreme cases.",
        'analyze_btn': "Analyze Stock",
        'analysis_header': "Analysis for",
        'sentiment': "Market Sentiment",
        'action': "Algorithmic Action",
        'anomalies_count': "Anomalies Detect",
        'tabs_price': "Price & Base Indicators",
        'tabs_tech': "Technical Momentum",
        'llm_header': "🤖 AI Analyst Interpretation",
        'anomalies_table': "View Detected Anomalies Detail",
        'no_anomalies': "No anomalies detected.",
        'generate_pdf': "Generate PDF Report",
        'download_pdf': "Download PDF",
        'error_api': "Error connecting to API",
        'warning_nodata': "No data available for the selected period after processing. Please try a longer date range.",
        'info_start': "Enter a ticker and click 'Analyze Stock' to begin."
    }
}

# Sidebar Inputs
st.sidebar.header("Configuration") # Will be updated with lang later, but header is static-ish

# Language Selector
lang_code = st.sidebar.radio("Language / Język", ['Polski', 'English'], index=0)
lang = 'pl' if lang_code == 'Polski' else 'en'
t = TRANSLATIONS[lang]

# Update static headers
st.title(t['title'])
st.markdown(t['subtitle'])
st.sidebar.header(t['config'])

market_options = [t['stock'], t['crypto']]
market_sel = st.sidebar.radio(t['market_type'], market_options)
market_type = "Stock" if market_sel == t['stock'] else "Crypto"

ticker_label = t['ticker_stock'] if market_type == "Stock" else t['ticker_crypto']
ticker_input = st.sidebar.text_input(ticker_label, value="AAPL" if market_type == "Stock" else "BTC")

if market_type == "Crypto" and not ticker_input.endswith("-USD"):
    ticker = f"{ticker_input.upper()}-USD"
else:
    ticker = ticker_input.upper()
today = date.today()
start_date = st.sidebar.date_input(t['start_date'], value=today - timedelta(days=365))
end_date = st.sidebar.date_input(t['end_date'], value=today)
contamination = st.sidebar.slider(t['sensitivity'], 0.01, 0.1, 0.05, 0.01, help=t['sensitivity_help'])

if st.sidebar.button(t['analyze_btn']):
    with st.spinner("Fetching data and analyzing..."):
        try:
            payload = {
                "ticker": ticker,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "contamination": contamination,
                "language": lang
            }
            response = requests.post(f"{API_URL}/analyze", json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Store data in session state for report generation
            st.session_state['analysis_result'] = result
            st.session_state['ticker'] = ticker
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to API: {e}")
            st.stop()

# Display Results if available
if 'analysis_result' in st.session_state:
    result = st.session_state['analysis_result']
    data = pd.DataFrame(result['data'])
    
    if data.empty:
        st.warning("No data available for the selected period after processing. Please try a longer date range.")
        st.stop()

    # 0. Algorithmic Verdict
    st.subheader(f"Analysis for {result['ticker']}")
    
    col1, col2, col3 = st.columns(3)
    
    sentiment = result.get('sentiment', 'NEUTRAL')
    action = result.get('action', 'HOLD')
    
    # Color logic
    s_color = "green" if sentiment == "BULLISH" else "red" if sentiment == "BEARISH" else "gray"
    a_color = "green" if "BUY" in action else "red" if "SELL" in action else "gray"
    
    col1.metric(label="Market Sentiment", value=sentiment, delta=None)
    # Using markdown for color since metric doesn't support custom text color easily
    col1.markdown(f":{s_color}[{sentiment}]") 
    
    col2.metric(label="Algorithmic Action", value=action)
    col2.markdown(f":{a_color}[{action}]")
    
    col3.metric(label="Anomalies Detect", value=result['anomalies_count'])

    # 1. Visualization
    st.markdown("---")
    
    # Create Candlestick
    # Tabs for visualization
    tab1, tab2 = st.tabs(["Price & Base Indicators", "Technical Momentum"])

    with tab1:
        # Create Candlestick with Bollinger Bands
        fig = go.Figure()
        
        # Candles
        fig.add_trace(go.Candlestick(
            x=data['date'],
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            name='Price'
        ))
        
        # Bollinger Bands
        if 'bb_upper' in data.columns and 'bb_lower' in data.columns:
            fig.add_trace(go.Scatter(x=data['date'], y=data['bb_upper'], line=dict(color='gray', width=1, dash='dash'), name='BB Upper'))
            fig.add_trace(go.Scatter(x=data['date'], y=data['bb_lower'], line=dict(color='gray', width=1, dash='dash'), name='BB Lower', fill='tonexty', fillcolor='rgba(200,200,200,0.1)'))
        
        # 50d MA
        if 'ma_50' in data.columns:
             fig.add_trace(go.Scatter(x=data['date'], y=data['ma_50'], line=dict(color='orange', width=2), name='MA 50'))

        # Add Anomalies
        anomalies = data[data['anomaly'] == -1]
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
                x=anomalies['date'],
                y=anomalies['close'],
                mode='markers',
                marker=dict(color='red', size=8, symbol='x'),
                name='Anomaly'
            ))
        
        fig.update_layout(xaxis_rangeslider_visible=False, height=600, title="Price Action with Bollinger Bands & MA50")
        st.plotly_chart(fig, width='stretch')

    with tab2:
        # RSI Chart
        if 'rsi' in data.columns:
            fig_rsi = go.Figure(go.Scatter(x=data['date'], y=data['rsi'], name='RSI', line=dict(color='purple')))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
            fig_rsi.update_layout(height=300, title="Relative Strength Index (RSI)")
            st.plotly_chart(fig_rsi, width='stretch')

        # MACD Chart
        if 'macd' in data.columns:
            fig_macd = go.Figure()
            # Assuming 'macd' col is the Histogram or Difference for now based on features.py
            fig_macd.add_trace(go.Bar(x=data['date'], y=data['macd'], name='MACD Hist'))
            fig_macd.update_layout(height=300, title="MACD Histogram")
            st.plotly_chart(fig_macd, width='stretch')
        
        # ADX
        if 'adx' in data.columns:
            fig_adx = go.Figure(go.Scatter(x=data['date'], y=data['adx'], name='ADX', line=dict(color='blue')))
            fig_adx.add_hline(y=25, line_dash="dot", annotation_text="Strong Trend")
            fig_adx.update_layout(height=300, title="ADX (Trend Strength)")
            st.plotly_chart(fig_adx, width='stretch')
            
        # Transaction Points on Tech Charts (RSI as canvas)
        # We can also add a dedicated "Signals" chart or overlay on RSI
        if 'action' in data.columns:
            # Filter buy/sell
            buys = data[data['action'] == 'BUY']
            sells = data[data['action'] == 'SELL']
            
            if 'rsi' in data.columns:
                # Add markers to RSI chart (re-using fig_rsi if possible, but streamlits runs sequentially)
                # We need to modify the RSI chart creation block above or add a new one. 
                # Let's add a Plotly overlay here for Signals if we want specific visibility.
                # Actually, best to add to the RSI figure above. simpler to just add markers here?
                # No, fig_rsi is local to that if block. 
                # Let's add a separate "Signals" track or just modify RSI block source?
                pass 
                
            # Let's re-create the RSI chart with signals properly
            if 'rsi' in data.columns:
                fig_sig = go.Figure()
                fig_sig.add_trace(go.Scatter(x=data['date'], y=data['rsi'], name='RSI', line=dict(color='purple')))
                fig_sig.add_hline(y=70, line_dash="dash", line_color="red")
                fig_sig.add_hline(y=30, line_dash="dash", line_color="green")
                
                # Add Buy markers
                if not buys.empty:
                    fig_sig.add_trace(go.Scatter(
                        x=buys['date'], y=buys['rsi'], mode='markers', 
                        marker=dict(color='green', size=10, symbol='triangle-up'), name='Buy Signal'
                    ))
                # Add Sell markers
                if not sells.empty:
                    fig_sig.add_trace(go.Scatter(
                        x=sells['date'], y=sells['rsi'], mode='markers', 
                        marker=dict(color='red', size=10, symbol='triangle-down'), name='Sell Signal'
                    ))
                    
                fig_sig.update_layout(height=350, title=f"RSI with Algo Signals ({t['action']})")
                st.plotly_chart(fig_sig, width='stretch')
    
    # 2. LLM Analysis
    st.subheader("🤖 AI Analyst Interpretation")
    st.info(result['llm_analysis'])
    
    # 3. Anomaly Table
    with st.expander("View Detected Anomalies Detail"):
        if not anomalies.empty:
            # Columns to display - handle missing cols gracefully
            cols = ['date', 'close', 'volume', 'rsi', 'vol_spike', 'atr', 'adx', 'stoch_k', 'obv']
            display_cols = [c for c in cols if c in anomalies.columns]
            st.dataframe(anomalies[display_cols])
        else:
            st.write("No anomalies detected.")

    # 4. Report Generation
    if st.button(t['generate_pdf']):
        with st.spinner("Generating PDF..."):
            try:
                # Filter anomalies again to send to report (simplified)
                anomalies_json = anomalies.to_json(orient='records')
                
                report_payload = {
                    "ticker": st.session_state['ticker'],
                    "analysis": result['llm_analysis'],
                    "anomalies_json": anomalies_json
                }
                
                report_res = requests.post(f"{API_URL}/report", json=report_payload)
                report_res.raise_for_status()
                
                st.download_button(
                    label="Download PDF",
                    data=report_res.content,
                    file_name=f"{st.session_state['ticker']}_Report.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Failed to generate report: {e}")

else:
    st.info("Enter a ticker and click 'Analyze Stock' to begin.")
