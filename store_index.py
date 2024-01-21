from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

FAISS_PATH = 'vectors/faiss_db'

def store_index(data):
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db = FAISS.from_documents(data,embedding=embeddings)
    db.save_local(FAISS_PATH)

    return db