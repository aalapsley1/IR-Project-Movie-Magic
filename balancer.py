def balance(keywords, movies, actors, query_scores, recommender_scores):
  """
  Balances the movie scores based on received data.

  Parameters:
    keywords:
      A list of keywords to query by.
      Example: ['Thriller']
    movies:
      A list of movies to recommend by.
      Example: ['The Dark Knight']
    actors:
      A list of actors to recommend by.
      Example: ['Morgan Freeman']
    query_scores:
      A dictionary of movie titles to scores normalized from -1 to 1.
      Example: {'The Quiet Place': 0.7, 'Frankenstein (1931)': 0.5, 'The Dark Knight': -0.2, 'Se7en': -0.3}
    recommender_scores:
      A dictionary of movie titles to scores. Should be normalized to range from -1 to 1. 
      Example: {'The Quiet Place': 0.2, 'Frankenstein (1931)': -0.5, 'The Dark Knight': 0.5, 'Se7en': 0.6}
    
  Returns: 
    A dictionary of movie titles to scores. These scores should be balanced between the queries and recommendations.  
    Should be normalized to range from -1 to 1. 
    Example: {'The Quiet Place': 0.3, 'Frankenstein (1931)': -0.1, 'The Dark Knight': 0.2, 'Se7en': 0.2}
  """
  
  final_scores = {}
  
  for q_movie in query_scores.keys():
    if q_movie in recommender_scores.keys():
      final_scores[q_movie] = (query_scores[q_movie] + recommender_scores[q_movie]) / 2
    else:
      final_scores[q_movie] = query_scores[q_movie] / 2
  
  for r_movie in recommender_scores.keys():
    if r_movie not in final_scores.keys():
      final_scores[r_movie] = recommender_scores[r_movie] / 2
  
  return final_scores
      
  