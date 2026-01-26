import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go  # NOUVEAU pour la jauge

# Configuration de la page
st.set_page_config(page_title="AI Decision System", layout="wide", page_icon="🧠")
API_URL = "http://127.0.0.1:8000"

st.title("🧠 AI Decision Support System")
st.markdown("---")

# Navigation
tab1, tab2, tab3 = st.tabs(["📈 Dashboard Stratégique", "🤖 Simulateur IA", "📄 Assistant Documentaire"])

# === ONGLET 1 : DASHBOARD STRATÉGIQUE ===
with tab1:
    st.header("Vue d'ensemble de l'activité")
    
    try:
        # 1. Chargement et Préparation
        df = pd.read_csv("backend/data/business_data.csv")
        df['date'] = pd.to_datetime(df['date'])
        
        # 2. Filtres
        col_filter, _ = st.columns([1, 3])
        with col_filter:
            years = sorted(df['date'].dt.year.unique(), reverse=True)
            selected_year = st.selectbox("📅 Année Fiscale", years, index=0)
        
        df_filtered = df[df['date'].dt.year == selected_year]
        
        # 3. KPIs
        total_rev = df_filtered['revenue'].sum()
        total_profit = df_filtered['profit'].sum()
        margin = (total_profit / total_rev * 100) if total_rev > 0 else 0
        marketing = df_filtered['marketing_spend'].sum()
        
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Chiffre d'Affaires", f"{total_rev:,.0f} €", delta="Cible atteinte")
        k2.metric("Profit Net", f"{total_profit:,.0f} €", delta=f"{margin:.1f}% Marge")
        k3.metric("Inv. Marketing", f"{marketing:,.0f} €", delta="Budget contrôlé")
        k4.metric("Clients Actifs", "1,240", delta="+12%") # Donnée fictive pour l'exemple
        
        st.markdown("---")
        
        # 4. Graphiques
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("💰 Performance Financière")
            fig_line = px.line(df_filtered, x='date', y=['revenue', 'profit'], 
                               color_discrete_map={"revenue": "#29b5e8", "profit": "#00CC96"})
            st.plotly_chart(fig_line, use_container_width=True)
            
        with c2:
            st.subheader("🎯 Efficacité Marketing")
            fig_scatter = px.scatter(df_filtered, x='marketing_spend', y='revenue', 
                                     size='profit', color='profit',
                                     color_continuous_scale="Viridis")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
    except Exception as e:
        st.error(f"Erreur de chargement des données : {e}")

# === ONGLET 2 : SIMULATEUR IA (UPGRADE PRO) ===
with tab2:
    st.header("🔮 Prédiction de Profit Future")
    st.markdown("Ajustez les leviers ci-dessous pour simuler la rentabilité future grâce au modèle **Machine Learning**.")
    
    col_input, col_viz = st.columns([1, 2])
    
    with col_input:
        st.subheader("Paramètres")
        with st.form("sim_form"):
            marketing_in = st.slider("Budget Marketing (€)", 0, 5000, 2000, step=100)
            stock_in = st.slider("Niveau de Stock (Unités)", 0, 500, 200, step=10)
            holiday_in = st.checkbox("Période de Vacances ?", value=False)
            
            submitted = st.form_submit_button("Lancer la Simulation", type="primary")
    
    with col_viz:
        st.subheader("Résultat de l'IA")
        if submitted:
            payload = {
                "marketing_spend": marketing_in, 
                "marketing_lag1": marketing_in, 
                "stock_available": stock_in, 
                "is_holiday": 1 if holiday_in else 0
            }
            
            try:
                res = requests.post(f"{API_URL}/predict", json=payload)
                if res.status_code == 200:
                    pred = res.json()['predicted_profit']
                    
                    # Jauge visuelle
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = pred,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Profit Estimé (€)"},
                        gauge = {
                            'axis': {'range': [None, 6000]},
                            'bar': {'color': "#00CC96" if pred > 3000 else "#FFB000"},
                            'steps': [
                                {'range': [0, 2000], 'color': "lightgray"},
                                {'range': [2000, 4000], 'color': "gray"}],
                        }
                    ))
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                    if pred > 3500:
                        st.success("🚀 Scénario très rentable !")
                    elif pred > 1500:
                        st.info("⚖️ Rentabilité moyenne.")
                    else:
                        st.warning("⚠️ Attention : Profit faible prévu.")
                else:
                    st.error("Erreur du modèle de prédiction.")
            except Exception as e:
                st.error(f"Impossible de contacter l'API : {e}")
        else:
            st.info("👈 Configurez les paramètres et lancez la simulation.")

# === ONGLET 3 : ASSISTANT DOCUMENTAIRE (RAG) ===
with tab3:
    st.header("📄 Chatbot Intelligent (RAG)")
    
    # Zone d'upload
    with st.expander("📂 Charger un nouveau document", expanded=True):
        uploaded_file = st.file_uploader("PDF requis (Rapports, Factures, CVs...)", type="pdf")
        if uploaded_file and st.button("Analyser ce document"):
            with st.spinner("Indexation en cours (Vectorisation)..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    res = requests.post(f"{API_URL}/upload-document", files=files)
                    if res.status_code == 200:
                        st.success("✅ Document analysé et mémorisé !")
                    else:
                        st.error(f"Erreur : {res.text}")
                except Exception as e:
                    st.error(f"Erreur de connexion : {e}")

    st.divider()
    
    # Interface de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("Posez votre question sur le document..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("L'IA réfléchit..."):
                try:
                    res = requests.post(f"{API_URL}/ask-document", json={"question": user_input})
                    if res.status_code == 200:
                        rep = res.json()["response"]
                        st.write(rep)
                        st.session_state.messages.append({"role": "assistant", "content": rep})
                    else:
                        st.error("Erreur du serveur RAG.")
                except Exception as e:
                    st.error(f"Erreur : {e}")