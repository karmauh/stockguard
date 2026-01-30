from fpdf import FPDF
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'StockGuard AI - Anomaly Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(ticker: str, analysis: str, anomalies_df: pd.DataFrame, file_path: str):
    pdf = PDFReport()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f'Analysis for: {ticker}', 0, 1)
    
    # Analysis Text
    pdf.set_font('Arial', '', 11)
    # FPDF doesn't support Markdown, so we strip/replace some formatting if needed or just dump text
    clean_analysis = analysis.replace('**', '').replace('\n\n', '\n')
    pdf.multi_cell(0, 8, clean_analysis)
    pdf.ln(5)
    
    # Anomalies Table
    if not anomalies_df.empty:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Detected Anomalies (Top 20)', 0, 1)
        
        pdf.set_font('Arial', 'B', 9) # Smaller font to fit more cols
        # Headers
        cols = ['Date', 'Close', 'RSI', 'VolSpike', 'ATR', 'ADX']
        # Widths: Date(30), Close(25), RSI(20), VolSpike(25), ATR(25), ADX(25) -> Total ~150 (A4 width is ~210, margins ~20)
        col_widths = [30, 25, 20, 25, 25, 25]
        
        for i, col in enumerate(cols):
            pdf.cell(col_widths[i], 10, col, 1)
        pdf.ln()
        
        pdf.set_font('Arial', '', 9)
        # Rows
        for _, row in anomalies_df.head(20).iterrows():
            date_str = str(row['date']).split()[0]
            close_str = f"{row['close']:.2f}"
            rsi_str = f"{row.get('rsi', 0):.2f}"
            vol_str = f"{row.get('vol_spike', 0):.2f}"
            atr_str = f"{row.get('atr', 0):.2f}"
            adx_str = f"{row.get('adx', 0):.2f}"
            
            data_row = [date_str, close_str, rsi_str, vol_str, atr_str, adx_str]
            
            for i, datum in enumerate(data_row):
                pdf.cell(col_widths[i], 10, datum, 1)
            pdf.ln()
            
    pdf.output(file_path)
