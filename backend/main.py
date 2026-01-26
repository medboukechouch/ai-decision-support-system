from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import joblib
import numpy as np
import shutil
import os
# Import du moteur RAG (assurez-vous que le fichier backend/rag_engine.py existe bien)
from backend.rag_engine import index_document, ask_question

app = FastAPI(title="AI Decision Support System", version="3.0 (RAG)")

# --- PARTIE 1 : MACHINE LEARNING (Sprint 2 & 3) ---
model = None
try:
    model = joblib.load("backend/ml/model.pkl")
except:
    print("⚠️ Modèle ML non trouvé. Pensez à lancer retrain_model.py")

class SimulationInput(BaseModel):
    marketing_spend: float
    marketing_lag1: float
    stock_available: int
    is_holiday: int 

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(data: SimulationInput):
    if not model:
        raise HTTPException(status_code=503, detail="Modèle ML non chargé")
    features = np.array([[data.marketing_spend, data.marketing_lag1, data.stock_available, data.is_holiday]])
    prediction = model.predict(features)[0]
    return {"predicted_profit": round(float(prediction), 2)}

# --- PARTIE 2 : RAG & DOCUMENTS (Sprint 4) ---

# Création du dossier temporaire pour les uploads s'il n'existe pas
os.makedirs("backend/documents", exist_ok=True)

class ChatInput(BaseModel):
    question: str

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Reçoit un PDF et lance l'indexation"""
    file_path = f"backend/documents/{file.filename}"
    
    # Sauvegarde physique du fichier
    with open(file_path, "wb+") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Indexation par le moteur RAG
    try:
        nb_chunks = index_document(file_path)
        return {"message": f"Document '{file.filename}' analysé ! ({nb_chunks} morceaux indexés)"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'analyse : {str(e)}")

@app.post("/ask-document")
def chat_with_document(data: ChatInput):
    """Pose une question à l'IA sur le document"""
    try:
        response = ask_question(data.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))