import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import faiss
import numpy as np

# File path for the movie data CSV
file_path = "movie_data.csv"

# Output path for Faiss index
faiss_index_path = "movie_faiss_index.faiss"

# Output path for movie metadata
metadata_path = "movie_metadata.csv"

try:
    # Read CSV data into a Pandas DataFrame
    df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip", engine="python")

    # Preprocess the data
    df["embedding_text"] = df["overview"].fillna("")

    # Load the embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Replace with your preferred model

    # Generate embeddings with a progress bar
    print("Generating embeddings...")
    movie_embeddings = []
    for text in tqdm(df["embedding_text"].tolist(), desc="Processing movies"):
        try:
            embedding = model.encode(text, convert_to_numpy=True)
            movie_embeddings.append(embedding)
        except Exception as e:
            print(f"Error generating embedding for text: {text}. Error: {e}")
            movie_embeddings.append(None)

    # Filter out rows with None embeddings
    df["embeddings"] = movie_embeddings
    valid_data = df[df["embeddings"].notnull()].reset_index(drop=True)

    # Convert embeddings into a NumPy array
    embeddings_matrix = np.vstack(valid_data["embeddings"].values)

    # Create a Faiss index
    index = faiss.IndexFlatL2(embeddings_matrix.shape[1])
    index.add(embeddings_matrix)

    # Save the Faiss index
    faiss.write_index(index, faiss_index_path)

    # Save the metadata
    valid_data.drop(columns=["embeddings"], inplace=True)
    valid_data.to_csv(metadata_path, index=False)

    print("Processing completed successfully.")

except Exception as e:
    print(f"An error occurred: {e}")