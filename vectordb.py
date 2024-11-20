import faiss
import numpy as np
import json

def create_faiss_database(data, vector_dimension=3072, index_path="faiss_index_3072.index", metadata_path="metadata_3072.json"):
    """
    Creates and saves a FAISS database using cosine similarity (normalized inner product)
    """
    # Extract embeddings and image paths
    embeddings = np.array([item[1] for item in data]).astype('float32')
    image_paths = [item[0] for item in data]
    
    # Normalize the vectors - this is crucial for cosine similarity
    faiss.normalize_L2(embeddings)  # In-place normalization
    
    # Create a FAISS index with Inner Product (equivalent to cosine similarity for normalized vectors)
    index = faiss.IndexFlatIP(vector_dimension)
    
    # Add normalized embeddings to the index
    index.add(embeddings)
    
    # Save the FAISS index
    faiss.write_index(index, index_path)
    
    # Save metadata
    metadata = {str(i): image_paths[i] for i in range(len(image_paths))}
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)
    
    print(f"FAISS database saved to {index_path}. Metadata saved to {metadata_path}.")

def query_faiss_database(query_vector, top_k=3, index_path="faiss_index_3072.index", metadata_path="metadata_3072.json"):
    """
    Queries the FAISS database using cosine similarity
    """
    # Load the FAISS index
    index = faiss.read_index(index_path)
    
    # Load metadata
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    
    # Convert query vector to float32 and reshape
    query_vector = np.array([query_vector]).astype('float32')
    
    # Normalize the query vector
    faiss.normalize_L2(query_vector)
    
    # Perform the search
    # With normalized vectors, higher IP scores (closer to 1) indicate more similarity
    similarities, indices = index.search(query_vector, top_k)
    
    # Retrieve the top-k image paths
    top_image_paths = [metadata[str(idx)] for idx in indices[0]]
    
    # Return both paths and similarity scores
    return list(zip(top_image_paths, similarities[0]))