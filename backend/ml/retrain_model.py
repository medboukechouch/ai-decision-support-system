import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

# 1. Chargement des données
# Ajustez le chemin si nécessaire selon où vous lancez le script
csv_path = "backend/data/business_data.csv"

if not os.path.exists(csv_path):
    print(f"ERREUR: Le fichier {csv_path} est introuvable.")
    exit()

df = pd.read_csv(csv_path)
print(f"✅ Données chargées : {len(df)} lignes")

# 2. Sélection stricte des 4 features du simulateur
features = ['marketing_spend', 'marketing_lag1', 'stock_available', 'is_holiday']
target = 'profit'

X = df[features]
y = df[target]

# 3. Entraînement du modèle simplifié (sans ColumnTransformer complexe)
model = LinearRegression()
model.fit(X, y)
print("✅ Modèle ré-entraîné avec succès sur 4 features.")

# 4. Écraser l'ancien modèle
model_path = "backend/ml/model.pkl"
joblib.dump(model, model_path)
print(f"✅ Nouveau modèle sauvegardé sous : {model_path}")