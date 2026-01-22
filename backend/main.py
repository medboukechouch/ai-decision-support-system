from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# -----------------------------
# Initialisation de l'API
# -----------------------------
app = FastAPI(
    title="AI Decision Support System",
    description="API de prédiction de profit business",
    version="1.0"
)

# -----------------------------
# Chargement du modèle ML
# -----------------------------
try:
    model = joblib.load("backend/ml/model.pkl")
except Exception as e:
    raise RuntimeError(f"Erreur chargement modèle: {e}")

# -----------------------------
# Schéma d'entrée (Request Body)
# -----------------------------
from pydantic import BaseModel

class PredictRequest(BaseModel):
    # Date brute (sera transformée)
    date: str

    # Categorical
    region: str
    product_category: str

    # Business metrics
    marketing_spend: float
    units_sold: int
    cost: float
    revenue: float

    # Pricing & stock
    price: float
    discount_rate: float
    stock_available: int
    out_of_stock: int

    # Marketing history
    marketing_lag1: float
    marketing_lag2: float

    # Calendar
    is_holiday: int



# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# Endpoint de prédiction
# -----------------------------
@app.post("/predict")
def predict(data: PredictRequest):
    try:
        # Conversion en DataFrame
        df = pd.DataFrame([data.dict()])

        # Conversion date
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.month
        df["day_of_week"] = df["date"].dt.dayofweek

        # On enlève la date brute
        df = df.drop(columns=["date"])

        # Prédiction
        prediction = model.predict(df)[0]

        return {
            "predicted_profit": round(float(prediction), 2)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# -----------------------------