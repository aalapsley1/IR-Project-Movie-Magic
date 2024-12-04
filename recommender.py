import math
from data import get_data
import numpy as np


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
  movie_indexes = []
  for id in movie_ids:
    movie_indexes.append(ratings_matrix.columns.get_loc(id))
  print(movie_indexes)
  
  correlations = np.corrcoef(ratings_matrix.T.values)
  print(correlations)
  
  ratings = []
  for corr in correlations:
    total_weight = 0
    total_rating = 0
    for i in movie_indexes:
      weight = corr[i]
      if (math.isnan(weight) or weight <= 0):
        continue
      
      total_weight += weight
      total_rating += weight * 10 

    if total_weight == 0:
      ratings.append(5)
    else:
      ratings.append(total_rating / total_weight)

  print(ratings)

  columns = list(ratings_matrix.columns)
  to_return = {}
  for i in range(columns):
    to_return[columns[i]] = ratings[i]

  return to_return


def main():
  
  data = get_data()
  
  example_movies_0 = ['The Shawshank Redemption']
  recommender_scores_0 = recommend(data, example_movies_0)
  
  print(recommender_scores_0)
  
  
if __name__ == "__main__":
  main()