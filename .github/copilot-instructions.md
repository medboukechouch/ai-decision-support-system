# AI Decision Support System – Developer Instructions

## Architecture Overview

This is a **3-tier machine learning & RAG system**:

1. **Backend (FastAPI)** – `backend/main.py` serves two core endpoints:
   - `/predict` – ML-based business analytics (integrates trained models from `backend/ml/`)
   - `/ask-document` – RAG interface for querying documents (LangChain + FAISS integration pending)

2. **Frontend (Streamlit)** – `frontend/app.py` provides interactive UI for:
   - Dataset upload and visualization
   - Natural language question input routed to backend endpoints

3. **Data Pipeline** – `backend/ml/generate_data.py` creates synthetic business data (sales, regions, categories) with `backend/data/business_data.csv` as source for exploration

## Data & ML Workflow

- **Data source**: `backend/data/business_data.csv` (1000 rows: dates, regions, product categories, marketing spend, units sold)
- **Feature relationships**: Region & category factors modulate marketing spend → units sold (see `generate_data.py` lines 26-48 for multiplier logic)
- **Expected ML task**: Regression (predict units_sold from marketing_spend + categorical features)
- **Model training**: Stub in `backend/ml/train_model.py` – implement sklearn pipeline with categorical encoding

## Critical Developer Workflows

**Running the system**:
```bash
# Terminal 1: Backend API
cd backend && python -m uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend && streamlit run app.py
```

**Data exploration**: Jupyter notebook at `notebooks/data_exploration.ipynb` (cell 1 loads CSV, cell 2 handles NaN values)

## Project-Specific Patterns

1. **Backend schemas**: Use `pydantic.BaseModel` in `main.py` for request validation (example: `PredictRequest` with `feature1`, `feature2`)
2. **Endpoint placeholders**: Endpoints marked with comments (e.g., `# placeholder ML`, `# placeholder RAG`) are incomplete – replace return values with actual logic
3. **Imports convention**: All backend dependencies in `requirements.txt` (fastapi, langchain, faiss-cpu, scikit-learn)

## Integration Points

- **FastAPI ↔ Streamlit**: Streamlit makes HTTP requests to FastAPI endpoints (implement in `frontend/app.py`)
- **ML ↔ API**: Trained model object must be loaded/cached in FastAPI before `/predict` call (pattern: load in app startup or endpoint function)
- **RAG components**: LangChain document loaders + FAISS index initialized in `/ask-document` handler

## Next Priority Tasks (from backlog.md)

1. Complete `backend/ml/train_model.py` with sklearn model training
2. Implement `/predict` endpoint logic integrating trained model
3. Connect Streamlit to backend endpoints via `requests` library
4. Implement `/ask-document` with LangChain FAISS integration

## File Reference Map

- Core API: [backend/main.py](backend/main.py)
- ML pipeline: [backend/ml/](backend/ml/)
- Frontend UI: [frontend/app.py](frontend/app.py)
- Data exploration: [notebooks/data_exploration.ipynb](notebooks/data_exploration.ipynb)
- Configuration: [requirements.txt](requirements.txt), [backlog.md](backlog.md)
