# 🧠 AI Decision Support System

Une plateforme complète d'aide à la décision pour entreprises, combinant **Machine Learning** (prédiction de ventes) et **IA Générative** (analyse de rapports PDF).

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)

## 🚀 Fonctionnalités Clés

1.  **📊 Dashboard Stratégique** : KPIs financiers en temps réel et visualisation de données interactives.
2.  **🔮 Simulateur IA** : Prédiction du profit futur avec jauge de performance (Modèle Random Forest).
3.  **📄 Assistant Documentaire (RAG)** : Chatbot intelligent capable de lire, comprendre et synthétiser vos PDF.

## 🛠️ Installation

1.  **Cloner le projet**
    ```bash
    git clone [https://github.com/ton-pseudo/ai-decision-support-system.git](https://github.com/ton-pseudo/ai-decision-support-system.git)
    cd ai-decision-support-system
    ```

2.  **Installer les dépendances**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration**
    Créez un fichier `.env` à la racine contenant :
    ```
    GOOGLE_API_KEY=votre_cle_api_ici
    ```

## ▶️ Démarrage

Lancez **deux terminaux** :

**Terminal 1 : API (Backend)**
```bash
python -m uvicorn backend.main:app --reload

```

**Terminal 2 : Interface (Frontend)**

```bash
streamlit run frontend/app.py

```

Accédez à l'application sur : `http://localhost:8501`

```

---

### 3. La Validation Finale (Git Push) 🚀

Une fois ces fichiers sauvegardés, lance les commandes magiques pour sceller ton projet :

```bash
git add .
git commit -m "Final Release: Complete AI Decision System with Dashboard, Sim & RAG"
git push origin main

```