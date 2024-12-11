from data import get_data
from recommender import recommend
from query import Query
from processor import Processor
from balancer import balance, id_to_title
import pandas as pd

def main():
  
  print("Getting data.")
  data = get_data()
  
  text = input('Enter your movie prompt: ')
  
  # # Send to GPT
  print("Processing text with gpt.")
  parseProc = Processor()
  parseProc.recvQuery(text)
  liked_movies = parseProc.getLikedMovies()
  disliked_movies = parseProc.getDislikedMovies()
  genres = parseProc.getGenres()
  keywords = parseProc.getKeywords()
  
  # liked_movies = ["Inception", "The Shawshank Redemption", "The Dark Knight", "Interstellar", "Parasite", "Whiplash", "The Matrix", "The Godfather", "Spirited Away", "The Grand Budapest Hotel"] 
  # disliked_movies = ["Transformers: Age of Extinction", "Twilight", "The Room", "Cats", "Battlefield Earth", "Fifty Shades of Grey", "Sharknado"] 
  # genres = ["Sci-Fi", "Thriller", "Action", "Crime", "Drama", "Comedy", "Animation", "Fantasy", "Adventure", "Romance", "Musical"] 
  # keywords = ["amazing", "deeply moving", "thrilling", "captivating", "mind-blowing", "brilliantly crafted", "intensely inspiring", "groundbreaking", "masterpiece", "enchanting", "delightfully quirky", "tedious", "overblown", "overly dramatic", "unimpressive", "laughable", "unbearable", "terrible", "awkward", "engaging"]

  # Get query scores
  print("Getting query scores.")
  movie_data = pd.read_csv("movie_data.csv")
  q = Query()
  query_scores = q.run_query(movie_data, genres, keywords)
  
  # Get recommender scores
  print("Getting recommender scores.")
  recommender_scores = recommend(data, liked_movies, disliked_movies)
  
  # Get final scores
  print("Balancing scores.")
  final_scores, other_scores = balance(query_scores, recommender_scores)
  
  # Print the top 5 movies.
  print("Getting top 5 movies.")
  sorted_movies = sorted(final_scores.keys(), key = lambda k: final_scores[k], reverse=True)
  
  final_recs = []
  
  if len(sorted_movies) < 10:
    sorted_others = sorted(other_scores.keys(), key = lambda k: other_scores[k], reverse=True)
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
  print("Top 5 movies:")
  print(final_recs_titles)
  
  return final_recs_titles

  
  

if __name__ == "__main__":
  main()