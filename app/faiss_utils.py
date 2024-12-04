import faiss
import numpy as np

# Initialize a FAISS index
class FaissIndex:
    def __init__(self, vector_size):
        # FAISS supports L2 distance by default
        self.index = faiss.IndexFlatL2(vector_size)
        self.chunk_metadata = []  # Store metadata like chunk_id and text

    def add_embeddings(self, embeddings, chunks):
        """
        Add embeddings to the FAISS index with metadata.
        :param embeddings: List of vectors (numpy arrays)
        :param chunks: List of text chunks corresponding to the embeddings
        """
        if len(embeddings) == 0:
            raise ValueError("No embeddings to add!")
        embeddings_array = np.array(embeddings).astype("float32")
        self.index.add(embeddings_array)

        # Add chunk metadata
        for i, chunk in enumerate(chunks):
            self.chunk_metadata.append({"chunk_id": i, "text": chunk})

    def search(self, query_vector, top_k=5):
        """
        Search the index for the most similar vectors.
        :param query_vector: Vector of the query text (numpy array)
        :param top_k: Number of top results to return
        :return: List of matched chunks
        """
        query_vector = np.array(query_vector).reshape(1, -1).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)
        results = [self.chunk_metadata[idx] for idx in indices[0] if idx < len(self.chunk_metadata)]
        return results
