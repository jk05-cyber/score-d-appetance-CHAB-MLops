"""FastAPI application for scoring service."""
from fastapi import FastAPI
from pydantic import BaseModel, conlist, Field
import pandas as pd

from ..models.predict import predict, load_model

app = FastAPI(title="CHAB Scoring API")

class ClientData(BaseModel):
    client_id: int
    age: float = Field(..., ge=0)
    tenure_days: float = Field(..., ge=0)
    n_products: int = Field(..., ge=0)
    sum_amount: float
    mean_amount: float

class BatchRequest(BaseModel):
    clients: conlist(ClientData, min_items=1)

class Prediction(BaseModel):
    client_id: int
    score: float
    probability: float
    prediction: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=Prediction)
def single_predict(data: ClientData):
    df = pd.DataFrame([data.dict()])
    result = predict(df, model=load_model())
    out = result.iloc[0].to_dict()
    out["client_id"] = data.client_id
    return out

@app.post("/batch_predict", response_model=list[Prediction])
def batch_predict(req: BatchRequest):
    df = pd.DataFrame([c.dict() for c in req.clients])
    preds = predict(df, model=load_model())
    preds["client_id"] = df["client_id"].values
    return preds.to_dict(orient="records")
