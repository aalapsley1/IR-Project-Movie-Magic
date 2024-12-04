import data

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
  
  users = data.get_users()
  
  
  return to_return