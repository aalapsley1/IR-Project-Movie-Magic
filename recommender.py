import math
import random

from surprise import Dataset, SVD, Reader
from surprise.model_selection import train_test_split
from data import get_data
import numpy as np
import pandas as pd


def recommend(data, good_movies, bad_movies):
  """
  Scores the movies based on similarity to user's liked movies.

  Parameters:
    data:
      The movie data to score.
    movies:
      A list of liked movies to recommend based on. 
      Example: ['The Shawshank Redemption']
    
  Returns: 
    A dictionary of movie ids to scores. Should be normalized to range from -1 to 1. 
    Example: {'the-dark-knight': 0.5, 'se7en': 0.6}
  """
  
  print("Starting recommender.")
  
  movies_export, ratings_export, _ = data

  # ratings_matrix = ratings_export.groupby(["user_id", "movie_id"]).rating_val.mean()
  # print(ratings_matrix)
  # ratings_matrix = ratings_matrix.unstack()
  # print(ratings_matrix)
    
  new_user_id = "zzz_new_user"
  new_user_user_ids = []
  new_user_movie_ids = []
  new_user_ratings = []
  for movie in good_movies:
    new_user_user_ids.append(new_user_id)
    new_user_movie_ids.append(movies_export[movies_export["movie_title"] == movie]["movie_id"].item())
    new_user_ratings.append(float(random.randint(8, 10)))
    
  for movie in bad_movies:
    new_user_user_ids.append(new_user_id)
    new_user_movie_ids.append(movies_export[movies_export["movie_title"] == movie]["movie_id"].item())
    new_user_ratings.append(float(random.randint(1, 3)))
    
  print("Prepare new user.")
    
  new_user_data = pd.DataFrame({"user_id": new_user_user_ids, "movie_id": new_user_movie_ids, "rating_val": new_user_ratings})

  ratings = pd.concat([ratings_export, new_user_data])
  
  print("Added new user.")
  
  reader = Reader(rating_scale=(1, 10))
  data = Dataset.load_from_df(ratings[["user_id", "movie_id", "rating_val"]], reader)
  trainset = data.build_full_trainset()
  model = SVD()
  model.fit(trainset)

  print("Generated model.")

  out = {}
  for movie_id in movies_export["movie_id"].tolist():
    pred = model.predict(new_user_id, movie_id, r_ui=4)
    out[movie_id] = (pred.est - 5.5) * 2 / 9
    
  print("Generated recommender scores.")

  return out


def main():
  
  data = get_data()
  
  example_movies_0 = ['The Dark Knight', 'Justice League'] 
  example_movies_1 = ['Jaws 2']
  recommender_scores_0 = run_and_print_info(data, example_movies_0, example_movies_1)
  
def run_and_print_info(data, good_movies, bad_movies):
  recommender_scores = recommend(data, good_movies, bad_movies)
  print("Ran recommender:")
  print("\tInput:")
  print(f"\t\tGood: {good_movies}")
  print(f"\t\tBad:  {bad_movies}")
  print("\tOutput:")
  highest_key = max(recommender_scores, key=recommender_scores.get)
  print(f"\t\tBest: {highest_key} - {recommender_scores[highest_key]}")
  lowest_key = min(recommender_scores, key=recommender_scores.get)
  print(f"\t\tWorst: {lowest_key} - {recommender_scores[lowest_key]}")
  
  return recommender_scores
  
  
if __name__ == "__main__":
  main()