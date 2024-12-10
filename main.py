from data import get_data
from recommender import recommend
from query import Query
from processor import tokenize
from balancer import balance

def main():
  
  movie_data, ratings_export, users_export = get_data()
  #movie_data = get_movies()
  
  text = input('Enter your movie prompt: ')
  
  genres, keywords, movies = tokenize(text)
  
  q = Query()
  query_scores = q.run_query(movie_data, genres, keywords)
  recommender_scores = recommend(movie_data, movies)
  
  scores = balance(keywords, movies, query_scores, recommender_scores)
  
  # Present the top 10 items or something.

if __name__ == "__main__":
  main()