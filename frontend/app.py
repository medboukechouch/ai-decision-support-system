import streamlit as st

st.title("AI Decision Support System")

st.header("Upload dataset")
uploaded_file = st.file_uploader("Choisir un CSV", type="csv")
if uploaded_file:
    st.write("Dataset uploadé !")

st.header("Ask a question")
question = st.text_input("Votre question")
if question:
    st.write(f"Réponse : {question} (à implémenter)")