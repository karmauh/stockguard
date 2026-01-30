from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from api.schemas import ReportRequest
from core.report import create_pdf_report
import pandas as pd
import json
import os
import uuid

router = APIRouter()

@router.post("/report")
def generate_report(request: ReportRequest):
    try:
        # Parse anomalies
        anomalies_data = json.loads(request.anomalies_json)
        anomalies_df = pd.DataFrame(anomalies_data)
        
        # Generate temporary filename
        filename = f"report_{uuid.uuid4()}.pdf"
        file_path = os.path.join("temp_reports", filename)
        os.makedirs("temp_reports", exist_ok=True)
        
        # Create PDF
        create_pdf_report(request.ticker, request.analysis, anomalies_df, file_path)
        
        return FileResponse(file_path, media_type='application/pdf', filename=f"{request.ticker}_Analysis_Report.pdf")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")
