import data
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
    A dictionary of movie titles to scores. Should be normalized to range from -1 to 1. 
    Example: {'The Dark Knight': 0.5, 'Se7en': 0.6}
  """
  to_return = {}
  
  # Get list of users and list of movies
  users, ratings_export = data.get_users()
  movies = data.get_movies()
  
  # Create array of ratings where:
  # ratings[i][j] is the movie movies[i] rating by user user[j]
  ratings = np.zeros((len(movies), len(users)))
  
        
  
  return to_return