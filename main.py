from data import get_data
from recommender import recommend
from query import query
from processor import tokenize
from balancer import balance

def main():
  
  data = get_data()
  
  text = input()
  
  genres, keywords, movies = tokenize(text)
  
  query_scores = query(data, genre, keywords)
  recommender_scores = recommend(data, movies)
  
  scores = balance(keywords, movies, actors, query_scores, recommender_scores)
  
  # Present the top 10 items or something.

if __name__ == "__main__":
  main()