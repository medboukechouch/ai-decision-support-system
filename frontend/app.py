import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="AI Decision System", layout="wide")
st.title("📊 AI Decision Support System")

# Chargement des données (Chemin relatif à la racine du projet)
try:
    df = pd.read_csv("backend/data/business_data.csv")
except Exception:
    st.warning("Données 'business_data.csv' introuvables. Mode dégradé.")
    df = pd.DataFrame()

# Onglets
tab1, tab2 = st.tabs(["📈 Dashboard", "🤖 Simulateur IA"])

with tab1:
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Chiffre d'Affaires", f"{df['revenue'].sum():,.0f} €")
        col2.metric("Profit Total", f"{df['profit'].sum():,.0f} €")
        
        # Graphique
        st.subheader("Évolution des Ventes")
        df['date'] = pd.to_datetime(df['date'])
        fig = px.line(df, x='date', y='revenue')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Veuillez générer les données pour voir le dashboard.")

with tab2:
    st.header("Prédire la rentabilité future")
    
    with st.form("sim_form"):
        c1, c2 = st.columns(2)
        with c1:
            marketing = st.number_input("Budget Marketing (€)", 500, 10000, 2000)
            marketing_lag = st.number_input("Marketing Veille (€)", 500, 10000, 2000)
        with c2:
            stock = st.number_input("Stock", 0, 5000, 200)
            holiday = st.checkbox("Période de vacances ?")
        
        submit = st.form_submit_button("Calculer le Profit")

    if submit:
        # Appel API
        payload = {
            "marketing_spend": marketing,
            "marketing_lag1": marketing_lag,
            "stock_available": stock,
            "is_holiday": 1 if holiday else 0
        }
        
        try:
            # Assurez-vous que l'URL correspond à votre uvicorn (souvent localhost:8000)
            res = requests.post("http://127.0.0.1:8000/predict", json=payload)
            if res.status_code == 200:
                profit = res.json()["predicted_profit"]
                st.success(f"💰 Profit Estimé : {profit:,.2f} €")
            else:
                st.error(f"Erreur API : {res.text}")
        except Exception as e:
            st.error(f"Connexion échouée : {e}")