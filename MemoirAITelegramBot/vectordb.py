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





def add_to_metadata(new_entry, data, vector_dimension=3072, index_path="faiss_index_3072.index", metadata_path="metadata_3072.json"):
    """
    Adds a new entry to the metadata JSON file and the FAISS index without overwriting existing data.

    Args:
        new_entry (tuple): A tuple containing (key, image_path), e.g., ("1", "path_to_image.jpg").
        data (list): A list of tuples where each tuple contains (image_path, embedding) to add to the FAISS index.
        metadata_path (str): Path to the metadata JSON file.
        index_path (str): Path to the FAISS index file.
    """
    # Extract embeddings and image paths
    embeddings = np.array([item[1] for item in data]).astype('float32')
    
    # Normalize the vectors - this is crucial for cosine similarity
    faiss.normalize_L2(embeddings)  # In-place normalization
    
    # Create a FAISS index with Inner Product (equivalent to cosine similarity for normalized vectors)
    index = faiss.IndexFlatIP(vector_dimension)
    
    # Add normalized embeddings to the index
    index.add(embeddings)
    
    # Save the FAISS index
    faiss.write_index(index, index_path)

    try:
        # Step 1: Read the existing metadata file, if it exists
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, create a new empty dictionary
            metadata = {}

        # Step 2: Add the new entry to the metadata dictionary
        key, image_path = new_entry  # This should be a tuple (key, image_path)
        metadata[key] = image_path

        # Step 3: Write the updated metadata back to the JSON file
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=4)

        print(f"Added new entry: {key} -> {image_path}")

    except Exception as e:
        print(f"Error adding to metadata: {e}")




# def query_faiss_database(query_vector, top_k=3, index_path="faiss_index_3072.index", metadata_path="metadata_3072.json"):
#     """
#     Queries the FAISS database using cosine similarity
#     """
#     # Load the FAISS index
#     index = faiss.read_index(index_path)
    
#     # Load metadata
#     with open(metadata_path, "r") as f:
#         metadata = json.load(f)
    
#     # Convert query vector to float32 and reshape
#     query_vector = np.array([query_vector]).astype('float32')
    
#     # Normalize the query vector
#     faiss.normalize_L2(query_vector)
    
#     # Perform the search
#     # With normalized vectors, higher IP scores (closer to 1) indicate more similarity
#     similarities, indices = index.search(query_vector, top_k)
    
#     # Retrieve the top-k image paths
#     top_image_paths = [metadata[str(idx)] for idx in indices[0]]
    
#     # Return both paths and similarity scores
#     return list(zip(top_image_paths, similarities[0]))

def query_faiss_database(query_vector, top_k=3, index_path="faiss_index_3072.index", metadata_path="metadata_3072.json"):
    """
    Queries the FAISS database using cosine similarity
    """
    try:
        # Load the FAISS index
        index = faiss.read_index(index_path)
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        return []
    
    # Load metadata
    try:
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return []
    
    # Convert query vector to float32 and reshape if necessary
    try:
        query_vector = np.array([query_vector]).astype('float32')
        if query_vector.ndim == 1:  # Ensure it's a 2D array for FAISS (batch of 1)
            query_vector = query_vector.reshape(1, -1)
    except Exception as e:
        print(f"Error converting query vector: {e}")
        return []

    # Normalize the query vector
    faiss.normalize_L2(query_vector)
    
    # Perform the search
    try:
        similarities, indices = index.search(query_vector, top_k)
    except Exception as e:
        print(f"Error during FAISS search: {e}")
        return []
    
    # Check if we have valid indices
    if indices.shape[0] == 0:
        print("No results found in FAISS index.")
        return []

    # Retrieve the top-k image paths
    try:
        top_image_paths = [metadata[str(idx)] for idx in indices[0] if str(idx) in metadata]
    except KeyError as e:
        print(f"Error retrieving image path for index {e}")
        return []
    
    # Return both paths and similarity scores
    return list(zip(top_image_paths, similarities[0]))
