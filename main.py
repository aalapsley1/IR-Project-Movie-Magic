from data import get_data
from recommender import recommend
from query import query
from processor import tokenize
from balancer import balance

def main():
  
  data = get_data()
  
  text = input()
  
  keywords, movies, actors = tokenize(text)
  
  query_scores = query(data, keywords)
  recommender_scores = recommend(data, movies, actors)
  
  scores = balance(keywords, movies, actors, query_scores, recommender_scores)

if __name__ == "__main__":
  main()