def recommend(data, movies, actors):
  """
  Scores the movies based on similarity to user's liked movie and actors.

  Parameters:
    data:
      The movie data to score.
    movies:
      A list of liked movies to recommend based on. 
      Example: ['The Shawshank Redemption']
    actors:
      A list of actors to recommend based on. 
      Example ['Morgan Freeman']
    
  Returns: 
    A dictionary of movie titles to scores. Should be normalized to range from -1 to 1. 
    Example: {'The Dark Knight': 0.5, 'Se7en': 0.6}
  """
  
  movie_data, ratings_export, users_export = get_data()
  
  return {}