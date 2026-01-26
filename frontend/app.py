import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Configuration
st.set_page_config(page_title="AI Decision System", layout="wide")
API_URL = "http://127.0.0.1:8000"

st.title("📊 AI Decision Support System")

# Onglets
tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "🤖 Simulateur Profit", "📄 Assistant Documentaire"])

# === ONGLET 1 : DASHBOARD ===
with tab1:
    try:
        df = pd.read_csv("backend/data/business_data.csv")
        col1, col2 = st.columns(2)
        col1.metric("Chiffre d'Affaires", f"{df['revenue'].sum():,.0f} €")
        col2.metric("Profit Total", f"{df['profit'].sum():,.0f} €")
        df['date'] = pd.to_datetime(df['date'])
        st.plotly_chart(px.line(df, x='date', y='revenue', title="Évolution des Ventes"), use_container_width=True)
    except:
        st.warning("Données introuvables.")

# === ONGLET 2 : SIMULATEUR ===
with tab2:
    st.header("Prédiction de Profit")
    with st.form("sim_form"):
        c1, c2 = st.columns(2)
        marketing = c1.number_input("Marketing (€)", 0, 10000, 2000)
        stock = c2.number_input("Stock", 0, 5000, 200)
        submit = st.form_submit_button("Calculer")
        
    if submit:
        payload = {"marketing_spend": marketing, "marketing_lag1": marketing, "stock_available": stock, "is_holiday": 0}
        res = requests.post(f"{API_URL}/predict", json=payload)
        if res.status_code == 200:
            st.success(f"Profit Estimé : {res.json()['predicted_profit']} €")
        else:
            st.error("Erreur API")

# === ONGLET 3 : RAG (NOUVEAU !) ===
with tab3:
    st.header("Discuter avec vos documents")
    
    # A. Upload de fichier
    uploaded_file = st.file_uploader("Chargez un rapport PDF (ex: Rapport Financier 2024)", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Analyser le document"):
            with st.spinner("L'IA lit le document..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                res = requests.post(f"{API_URL}/upload-document", files=files)
                if res.status_code == 200:
                    st.success(res.json()["message"])
                else:
                    st.error(f"Erreur : {res.text}")

    st.divider()
    
    # B. Interface de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Afficher l'historique
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Zone de saisie
    user_input = st.chat_input("Posez une question sur le document...")
    
    if user_input:
        # 1. Affiche la question utilisateur
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # 2. Appel API pour la réponse
        # ... (dans frontend/app.py, vers la ligne 87) ...
        
        # 2. Appel API pour la réponse
        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                try:
                    res = requests.post(f"{API_URL}/ask-document", json={"question": user_input})
                    
                    if res.status_code == 200:
                        # Tout va bien
                        ai_response = res.json()["response"]
                        st.write(ai_response)
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    else:
                        # ERREUR : On affiche le détail technique renvoyé par FastAPI
                        try:
                            error_detail = res.json().get("detail", res.text)
                        except:
                            error_detail = res.text
                        st.error(f"Erreur du serveur ({res.status_code}) : {error_detail}")
                        
                except Exception as e:
                    st.error(f"Erreur de connexion : {e}")