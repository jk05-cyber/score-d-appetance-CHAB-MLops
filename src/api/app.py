"""FastAPI application for scoring service."""
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from typing import Any, Dict, List

from ..models.predict import predict, load_model

app = FastAPI(title="CHAB Scoring API")

@app.get("/")
def root():
    return {"message": "Welcome to CHAB Scoring API", "docs": "/docs", "health": "/health"}

class ClientPrediction(BaseModel):
    client_id: int
    score: float
    probability: float
    prediction: int

class BatchPredictionRequest(BaseModel):
    features: List[Dict[str, Any]]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=ClientPrediction)
def single_predict(features: Dict[str, Any]):
    """Score a single client given feature values.
    
    Example:
    {
        "n_products": 2,
        "sum_amount": 5000.0,
        "mean_amount": 2500.0,
        "std_amount": 1500.0,
        "n_transactions": 10,
        "net_flow": 3000.0,
        "tenure_days": 365,
        "socio_pro_idx": 0,
        "AGE": 35,
        "SEXE": "M"
    }
    """
    df = pd.DataFrame([features])
    # Drop client_id if present to avoid feature mismatch
    if "client_id" in df.columns:
        client_id = df["client_id"].iloc[0]
        df = df.drop(columns=["client_id"])
    else:
        client_id = features.get("ID_CLIENT", -1)
    
    result = predict(df, model=load_model())
    out = result.iloc[0].to_dict()
    out["client_id"] = client_id
    return out

@app.post("/batch_predict", response_model=List[ClientPrediction])
def batch_predict(req: BatchPredictionRequest):
    """Score multiple clients in batch.
    
    Request body:
    {
        "features": [
            {"n_products": 2, "sum_amount": 5000, ...},
            {"n_products": 3, "sum_amount": 7000, ...}
        ]
    }
    """
    df = pd.DataFrame(req.features)
    client_ids = df["client_id"].values if "client_id" in df.columns else df["ID_CLIENT"].values if "ID_CLIENT" in df.columns else range(len(df))
    
    if "client_id" in df.columns:
        df = df.drop(columns=["client_id"])
    if "ID_CLIENT" in df.columns:
        df = df.drop(columns=["ID_CLIENT"])
    
    preds = predict(df, model=load_model())
    preds["client_id"] = client_ids
    return preds.to_dict(orient="records")
