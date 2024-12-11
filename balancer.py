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
  
  # Change movie_id to movie_title
  movie_data = pd.read_csv("movie_data.csv")
  r_scores = {}
  q_scores = {}
  
  for rec in recommender_scores.keys():
    for index,row in movie_data.iterrows():
      if rec == row['movie_id']:
          r_scores[row['movie_title']] = recommender_scores[rec]
          break
  
  for q in query_scores.keys():
    for index,row in movie_data.iterrows():
      if q == row['movie_id']:
          q_scores[row['movie_title']] = query_scores[q]
          break
  
  
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
  q_scores = {'i-lost-my-m-in-vegas': 0.5, 'how-will-you-die': 0.1, 'drillbit': -0.3, 'circus-savage': -0.7, 'the-art-of-filmmaking': 0.8}
  r_scores = {'i-lost-my-m-in-vegas': 0.3, 'drillbit': 0.5, 'circus-savage': -0.5, 'the-bus-1961': 0.3}
  f_scores, o_scores = balance(q_scores, r_scores)
  print(f_scores)
  print(o_scores)
  
  sorted_movies = sorted(f_scores.keys(), key = lambda k: f_scores[k], reverse=True)
  
  if len(sorted_movies) < 5:
    sorted_others = sorted(o_scores.keys(), key = lambda k: o_scores[k], reverse=True)
    to_print = ''
    i = 0
    for movie in sorted_movies:
      to_print += str(i + 1) + '. ' + movie + '\n'
      i += 1
    for omovie in sorted_others:
      if i >= 5:
        break
      to_print += str(i + 1) + '. ' + omovie + '\n'
      i += 1
  else:
    for i in range(5):
      to_print += str(i + 1) + '. ' + sorted_movies[i] + '\n'
  
  print(to_print)
  
if __name__ == "__main__":
  main()