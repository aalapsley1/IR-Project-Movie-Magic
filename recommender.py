import math
from data import get_data
import numpy as np
import pandas as pd


def recommend(data, movies):
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
  
  movies_export, ratings_export, _ = data

  ratings_matrix = ratings_export.groupby(["user_id", "movie_id"]).rating_val.mean()
  print(ratings_matrix)
  ratings_matrix = ratings_matrix.unstack()
  print(ratings_matrix)
  
  movie_ids = []
  for movie in movies:
    movie_ids.append(movies_export[movies_export["movie_title"] == movie]["movie_id"].item())
  print(movie_ids)
  # movie_indexes = []
  # for id in movie_ids:
  #   movie_indexes.append(ratings_matrix.columns.get_loc(id))
  # print(movie_indexes)
  
  # num_cols = ratings_matrix.shape[1]
  
  # new_user = np.full([num_cols], np.nan)
  # new_user[1] = 10.0
  # for index in movie_indexes:
  #   new_user[index] = 10.0
  # print(new_user)
  
  new_user_id = "zzz_new_user"
  new_user = {}
  for id in movie_ids:
    new_user[id] = 10.0
  
  new_user = pd.DataFrame(new_user, index=[new_user_id])
  ratings_matrix = pd.concat([ratings_matrix, new_user])
  print(ratings_matrix)
  
  correlations = np.corrcoef(ratings_matrix.values)
  print(correlations)

  return {}


def main():
  
  data = get_data()
  
  example_movies_0 = ['The Shawshank Redemption']
  recommender_scores_0 = recommend(data, example_movies_0)
  
  print(recommender_scores_0)
  
  
if __name__ == "__main__":
  main()