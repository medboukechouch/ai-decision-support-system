import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 1. Chargement de la clé API
load_dotenv()   
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("❌ Erreur : La clé GOOGLE_API_KEY est introuvable dans le fichier .env")

# 2. Configuration Hybride
# A. Le Cerveau (Gemini - Cloud)
# On revient au nom standard. Comme les embeddings sont locaux, ça ne plantera plus !
llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0.3)

# B. La Mémoire (Local)
# Le petit modèle rapide pour lire les PDF sans quota Google
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Variable globale
vector_store = None

def index_document(file_path: str):
    """Lit un PDF, le découpe et crée l'index de recherche."""
    global vector_store
    
    # A. Chargement
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    # B. Découpage
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    # C. Indexation Vectorielle (Locale)
    vector_store = FAISS.from_documents(documents=splits, embedding=embeddings)
    
    return len(splits)

def ask_question(question: str):
    """Interroge le document."""
    global vector_store
    
    if not vector_store:
        return "⚠️ Aucun document n'a été chargé. Veuillez uploader un PDF d'abord."
    
    # A. Récupérateur
    retriever = vector_store.as_retriever()
    
    # B. Prompt
    system_prompt = (
        "Tu es un assistant expert pour l'analyse de documents. "
        "Utilise le contexte ci-dessous pour répondre à la question. "
        "Si tu ne sais pas, dis-le."
        "\n\n"
        "--- Contexte ---\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])
    
    # C. Formatage
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # D. Chaîne RAG
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain.invoke(question)