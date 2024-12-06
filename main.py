from data import get_data
from recommender import recommend
from query import query
from processor import tokenize
from balancer import balance

def main():
  
  data = get_data()
  
  text = input('Enter your movie prompt: ')
  
  genres, keywords, good_movies, bad_movies = tokenize(text)
  
  query_scores = query(data, genres, keywords)
  recommender_scores = recommend(data, good_movies, bad_movies)
  
  scores = balance(keywords, movies, query_scores, recommender_scores)
  
  # Present the top 10 items or something.

if __name__ == "__main__":
  main()