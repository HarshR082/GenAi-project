from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = []
        self.text_chunks = []
        self.index = None

    def add_text_chunks(self, chunks):
        self.text_chunks = chunks
        self.embeddings = self.model.encode(chunks)
        d = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(self.embeddings)

    def retrieve(self, query, top_k=3):
        q_emb = self.model.encode([query])
        D, I = self.index.search(q_emb, top_k)
        return [self.text_chunks[i] for i in I[0]]
