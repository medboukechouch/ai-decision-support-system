from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Decision Support System")

# Schema pour prédiction
class PredictRequest(BaseModel):
    feature1: float
    feature2: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: PredictRequest):
    # placeholder ML
    return {"prediction": 0}

@app.get("/analyze")
def analyze():
    return {"message": "Analyse à implémenter"}

@app.post("/ask-document")
def ask_document(question: str):
    # placeholder RAG
    return {"answer": "RAG à implémenter"}