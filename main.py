from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from data import get_data
from recommender import recommend
from query import Query
from processor import Processor
from balancer import balance, id_to_title
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allow all origins by default, or configure as needed


@app.route('/recommend', methods=['POST'])
def recommend_movies():
    # Get the user input from the request
    user_input = request.form.get("user_prompt")


    format = """
        You are a movie recommendation assistant. Your task is to parse user queries and organize the data into four distinct categories: 1. Liked Movies: Movies the user mentions they like or want something similar to. 2. Disliked Movies: Movies the user mentions they dislike or want to avoid. 3. Genres: Translate adjectives or phrases in the query into movie genres (e.g., "funny" to "Comedy", "heartwarming" to "Drama"). Use known movie genres wherever applicable. 4. Keywords: Extract relevant adjectives or descriptive phrases from the query exactly as stated, even if they don't map directly to a genre. Format the output as follows: [["Liked Movies": ["..."], "Disliked Movies": ["..."], "Genres": ["..."], "Keywords": ["..."]. Here is the query: "
    """

    text = format + user_input

    # # Make a POST request to the other API
    response = requests.post('http://127.0.0.1:5110/api/prompt_route', json={'user_prompt': text})
    response_data = response.json()

    # # Extract the Answer field from the response
    answer_string = response_data.get('Answer', '')


    # Get data
    data = get_data()

    # Process text with GPT
    parseProc = Processor()
    parseProc.recvQuery(answer_string)
    liked_movies = parseProc.liked_movies
    disliked_movies = parseProc.disliked_movies
    genres = parseProc.genres
    keywords = parseProc.keywords

    # liked_movies = ["Inception", "The Shawshank Redemption", "The Dark Knight", "Interstellar", "Parasite", "Whiplash", "The Matrix", "The Godfather", "Spirited Away", "The Grand Budapest Hotel"] 
    # disliked_movies = ["Transformers: Age of Extinction", "Twilight", "The Room", "Cats", "Battlefield Earth", "Fifty Shades of Grey", "Sharknado"] 
    # genres = ["Sci-Fi", "Thriller", "Action", "Crime", "Drama", "Comedy", "Animation", "Fantasy", "Adventure", "Romance", "Musical"] 
    # keywords = ["amazing", "deeply moving", "thrilling", "captivating", "mind-blowing", "brilliantly crafted", "intensely inspiring", "groundbreaking", "masterpiece", "enchanting", "delightfully quirky", "tedious", "overblown", "overly dramatic", "unimpressive", "laughable", "unbearable", "terrible", "awkward", "engaging"]

    # Get query scores
    movie_data = pd.read_csv("movie_data.csv")
    q = Query()
    query_scores = q.run_query(movie_data, genres, keywords)

    # Get recommender scores
    recommender_scores = recommend(data, liked_movies, disliked_movies)

    # Get final scores
    final_scores, other_scores = balance(query_scores, recommender_scores)

    # Get the top 10 movies
    sorted_movies = sorted(final_scores.keys(), key=lambda k: final_scores[k], reverse=True)

    final_recs = []

    if len(sorted_movies) < 10:
        sorted_others = sorted(other_scores.keys(), key=lambda k: other_scores[k], reverse=True)
        i = len(sorted_movies)
        j = 0
        final_recs = sorted_movies
        while i < 10:
            final_recs.append(sorted_others[j])
            i += 1
            j += 1
    else:
        final_recs = sorted_movies[:10]

    final_recs_titles = [id_to_title(movie) for movie in final_recs]
    print(final_recs)
    return jsonify({"top": final_recs_titles})

if __name__ == "__main__":
    app.run(debug=True, port=5001)