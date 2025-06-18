import os
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import pickle

class VectorStore:
  def __init__(self, persist_directory="data/processed/vectorstore"):
    """Initialise vector store with the given persistence directory."""
    self.persist_directory = persist_directory
    self.embeddings = OpenAIEmbeddings()
    os.makedirs(persist_directory, exist_ok=True)

  def create_from_documents(self, documents: List[Dict[str, Any]]):
    """Create vector store from document chunks."""
    texts = [doc["content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]
    
    vectorstore = Chroma.from_texts(
      texts=texts,
      embedding=self.embeddings,
      metadatas=metadatas,
      persist_directory=self.persis_directory
    )
    vectorstore.persist()
    return vectorstore

  def load(self):
    """Load existing vector store from disk."""
    if not os.path.exists(self.persist_directory):
      raise FileNotFoundError(f"Vector store directory not found: {self.persist_directory}")
  
    return Chroma(
      persist_directory=self.persist_directory,
      embedding_function=self.embeddings
    )
  
  def query(self, query: str, k: int = 5):
    """Query the vector store for relevant document chunks."""
    vectorstore = self.load()
    return vectorstore.similarity_search(query, k=k)

if __name__ == "__main__":
  # Example usage
  from document_processor import DocumentProcessor

  processor = DocumentProcessor()
  chunks = processor.process_document("data/cps230.pdf", "data/processed")

  vectorstore = VectorStore()
  vectorstore.create_from_documents(chunks)
  print("Vector store created successfully")
