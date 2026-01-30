from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import analyze, report

app = FastAPI(title="StockGuard AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api")
app.include_router(report.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
