from data import get_data
from recommender import recommend
import query
from processor import tokenize
from balancer import balance

def main():
  
  data = get_data()
  
  text = input('Enter your movie prompt: ')
  
  # Send to GPT
  
  # GPT outputs
  liked_movies, disliked_movies, genres, keywords = []

  # Get query scores
  q = query.Query(genres, keywords)
  query_scores = q.query()
  
  # Get recommender scores
  recommender_scores = recommend(liked_movies, disliked_movies)
  
  # Get final scores
  final_scores, other_scores = balance(query_scores, recommender_scores)
  
  # Print the top 5 movies.
  sorted_movies = sorted(final_scores.keys(), key = lambda k: final_scores[k], reverse=True)
  
  if len(sorted_movies) < 5:
    sorted_others = sorted(other_scores.keys(), key = lambda k: other_scores[k], reverse=True)
    to_print = ''
    i = 0
    for movie in sorted_movies:
      to_print += str(i) + '. ' + movie + '\n'
      i += 1
    for omovie in sorted_others:
      if i >= 5:
        break
      to_print += str(i) + '. ' + omovie + '\n'
      i += 1
  else:
    for i in range(5):
      to_print += str(i) + '. ' + sorted_movies[i] + '\n'
  
  print(to_print)
  

if __name__ == "__main__":
  main()