from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import numpy as np

app = FastAPI(
    title="AI Decision Support System",
    version="2.0"
)

# Chargement du modèle
try:
    # Assurez-vous que le chemin est correct selon votre structure
    model = joblib.load("backend/ml/model.pkl")
except Exception:
    # Fallback pour éviter le crash si le pkl n'est pas trouvé immédiatement
    model = None
    print("⚠️ Modèle non trouvé. Lancez l'entraînement d'abord.")

# --- CORRECTION MAJEURE : On ne demande que les paramètres de simulation ---
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
        raise HTTPException(status_code=503, detail="Modèle non chargé")
    
    # On prépare les features dans l'ordre exact de l'entraînement
    # Note: Le modèle attendait peut-être un DataFrame ou un array. 
    # Ici on passe un array simple correspondant aux 4 features clés.
    features = np.array([[
        data.marketing_spend, 
        data.marketing_lag1, 
        data.stock_available, 
        data.is_holiday
    ]])
    
    try:
        prediction = model.predict(features)[0]
        return {"predicted_profit": round(float(prediction), 2)}
    except Exception as e:
        # Si le modèle a été entraîné avec plus de colonnes (ex: region, date...), 
        # il faudra ré-entraîner le modèle avec SEULEMENT ces 4 colonnes.
        raise HTTPException(status_code=500, detail=f"Erreur modèle: {str(e)}")