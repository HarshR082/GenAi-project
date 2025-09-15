import numpy as np

class VectorStore:
    def __init__(self, embeddings=None):
        # embeddings should be a 2D numpy array
        self.embeddings = embeddings if embeddings is not None else np.empty((0, 0))
        self.text_chunks = []

    def add_text_chunks(self, chunks):
        """
        Add text chunks and generate embeddings safely.
        """
        from some_embedding_module import embed_text  # replace with your embedding function

        new_embeddings = []
        for chunk in chunks:
            vector = embed_text(chunk)  # returns 1D array
            if vector is not None and len(vector) > 0:
                new_embeddings.append(vector)
                self.text_chunks.append(chunk)

        if len(new_embeddings) == 0:
            raise ValueError("No embeddings were generated. Check chunking or embedding function.")

        new_embeddings = np.vstack(new_embeddings)
        if self.embeddings.size == 0:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
