import pandas as pd
import numpy as np

# -----------------------------
# Paramètres
# -----------------------------
N_ROWS = 1000
np.random.seed(42)

# Dates sur 2 ans
dates = pd.date_range(start='2022-01-01', periods=N_ROWS, freq='D')

# Régions
regions = ['North', 'South', 'East', 'West']
region = np.random.choice(regions, size=N_ROWS)

# Catégories produits
categories = ['Electronics', 'Clothing', 'Home', 'Food']
product_category = np.random.choice(categories, size=N_ROWS)

# Prix moyen + discount
price_per_unit = {
    "Electronics": 300,
    "Clothing": 50,
    "Home": 120,
    "Food": 20
}
discount_rate = np.random.uniform(0, 0.2, N_ROWS)  # 0 à 20% discount
price = np.array([price_per_unit[c] for c in product_category])
price = price * (1 - discount_rate)

# Marketing spend avec lag
marketing_spend = np.random.randint(500, 5000, N_ROWS)
marketing_lag1 = np.roll(marketing_spend, 1)
marketing_lag2 = np.roll(marketing_spend, 2)
marketing_lag1[0:2] = marketing_spend[0:2]  # gérer les 2 premiers
marketing_lag2[0:2] = marketing_spend[0:2]

# Stock
stock_available = np.random.randint(50, 500, N_ROWS)
out_of_stock = np.random.binomial(1, 0.05, N_ROWS)  # 5% out of stock

# Saison / vacances
month = pd.Series(dates).dt.month
is_holiday = month.isin([1,7,12]).astype(int)  # exemple : vacances

# -----------------------------
# Units sold (fonction complexe)
# -----------------------------
units_sold = (
    0.5*marketing_spend +
    0.3*marketing_lag1 +
    0.2*marketing_lag2 +
    50*(1 - out_of_stock) +
    10*is_holiday +
    np.random.normal(0, 20, N_ROWS)
).astype(int)

units_sold = np.maximum(units_sold, 1)
units_sold = np.minimum(units_sold, stock_available)  # can't sell more than stock

# -----------------------------
# Revenue, cost et profit
# -----------------------------
revenue = units_sold * price
cost = revenue * np.random.uniform(0.6, 0.85, N_ROWS)  # marge variable
profit = revenue - cost

# -----------------------------
# Création du DataFrame
# -----------------------------
df = pd.DataFrame({
    "date": dates,
    "region": region,
    "product_category": product_category,
    "price": price,
    "discount_rate": discount_rate,
    "marketing_spend": marketing_spend,
    "marketing_lag1": marketing_lag1,
    "marketing_lag2": marketing_lag2,
    "stock_available": stock_available,
    "out_of_stock": out_of_stock,
    "units_sold": units_sold,
    "revenue": revenue,
    "cost": cost,
    "profit": profit,
    "is_holiday": is_holiday
})

# -----------------------------
# Sauvegarde
# -----------------------------
df.to_csv("backend/data/business_data.csv", index=False)
print("✅ Dataset business_data.csv généré avec succès !")
