import pandas as pd

def balance(query_scores, recommender_scores):
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
  
  r_scores = recommender_scores # {}
  q_scores = query_scores # {}
  
  # Averaging scores of movies appearing in both lists
  final_scores = {}
  other_scores = {}

  for q_movie in q_scores.keys():
    if q_movie in r_scores.keys():
      final_scores[q_movie] = (q_scores[q_movie] + r_scores[q_movie]) / 2
    else:
      other_scores[q_movie] = q_scores[q_movie] * 0.5
  
  # Storing scores of movies only in one of the lists, dampening by 0.5 (query above, rec below)
  for r_movie in r_scores.keys():
    if r_movie not in final_scores.keys():
      other_scores[r_movie] = r_scores[r_movie] * 0.5
  
  return final_scores, other_scores

      
def main():
  final_scores = {'i-lost-my-m-in-vegas': 0.5, 'how-will-you-die': 0.1, 'drillbit': -0.3, 'circus-savage': -0.7, 'the-art-of-filmmaking': 0.8, 'the-cartographer': 0.5}
  other_scores = {'elements-of-nothing': 0.3, 'a-mal-gam-a': 0.5, 'give-us-the-moon': -0.5, 'the-bus-1961': 0.3, 'lil-spider-girl': 0.9}
  
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
  print(final_recs_titles)

def id_to_title(id):
  movie_data = pd.read_csv("movie_data.csv")
  
  for index,row in movie_data.iterrows():
    if id == row['movie_id']:
      return row['movie_title']
      
  
if __name__ == "__main__":
  main()