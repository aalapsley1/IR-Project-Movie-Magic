from flask import Flask, jsonify, request
from flask_cors import CORS
import faiss
import numpy as np
import pickle
import math

app = Flask(__name__)
CORS(app)  # Allow all origins by default, or configure as needed

# Load your Faiss index
INDEX_PATH = '/Users/amangupta/Documents/GitHub/localGPT/IrProject/movie_faiss_index.faiss'
METADATA_PATH = '/Users/amangupta/Documents/GitHub/localGPT/IrProject/metadata.pkl'

index = faiss.read_index(INDEX_PATH)

# Load metadata (assumed to be stored as a pickle file)
with open(METADATA_PATH, 'rb') as f:
    metadata = pickle.load(f)

def replace_nan_with_empty_string(data):
    if isinstance(data, dict):
        return {k: ("" if isinstance(v, float) and math.isnan(v) else v) for k, v in data.items()}
    return data

@app.route('/movies', methods=['GET'])
def get_movies():
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    # Calculate start and end indices
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    # Slice metadata
    paginated_metadata = metadata[start_idx:end_idx]

    # Replace NaN values with empty strings
    paginated_metadata = [replace_nan_with_empty_string(movie) for movie in paginated_metadata]

    # Return paginated metadata
    return jsonify(paginated_metadata)

@app.route('/search', methods=['GET'])
def search():
    # Get search parameters from the request
    genre = request.args.get('genre', None)
    title = request.args.get('title', None)
    year = request.args.get('year', None)
    language = request.args.get('language', None)
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))

    # Filter metadata based on the provided parameters
    filtered_metadata = metadata

    if genre and genre.strip():
        genre = genre.lower()
        filtered_metadata = [movie for movie in filtered_metadata if isinstance(movie.get('genres', []), list) and any(g.lower() == genre for g in movie.get('genres', []))]

    if title and title.strip():
        title = title.lower()
        filtered_metadata = [movie for movie in filtered_metadata if isinstance(movie.get('movie_title', ''), str) and title in movie.get('movie_title', '').lower()]

    if year and year.strip():
        try:
            year = int(year)
            filtered_metadata = [movie for movie in filtered_metadata if movie.get('year_released') == year]
        except ValueError:
            pass

    if language and language.strip():
        language = language.lower()
        filtered_metadata = [movie for movie in filtered_metadata if isinstance(movie.get('original_language', ''), str) and language in movie.get('original_language', '').lower()]

    # Pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    # Slice metadata
    paginated_metadata = filtered_metadata[start_idx:end_idx]

    # Replace NaN values with empty strings
    paginated_metadata = [replace_nan_with_empty_string(movie) for movie in paginated_metadata]

    # Return paginated metadata
    return jsonify(paginated_metadata)



if __name__ == '__main__':
    app.run(port=5000)