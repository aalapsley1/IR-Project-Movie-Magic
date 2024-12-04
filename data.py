import pandas as pd
import kagglehub

# Download latest version



def download_data():

  '''
  Ok, I cannot figure out how to not have this download to a random location, 
  So it downloads to wherever it feels, and then prints out the location
  Find it, move the three files into this folder, and then get_data
  '''
  path = kagglehub.dataset_download("samlearner/letterboxd-movie-ratings-data")
  print("Path to dataset files:", path)
  pass


def get_data():

  """
  Loads and returns the data in panda dataframes.
  """

  movie_data = pd.read_csv("movie_data.csv")
  movie_data = movie_data.drop(["imdb_id","imdb_link", "image_url", "tmdb_id", "tmdb_link"], axis = 1)
  ratings_export = pd.read_csv("ratings_export.csv")
  users_export = pd.read_csv("users_export.csv")
  


  return movie_data, ratings_export, users_export

def get_users():
  
  """
  Returns list of users from ratings data
  """
  
  ratings_export = pd.read_csv("ratings_export.csv")
  
  users = []
  i = 0
  for user in ratings_export['user_id']:
    if user not in users:
      users.append(user)
    # Progress tracker
    i += 1
    if i % 500000 == 0:
      print(str(round((i / 11078167) * 100)) + '%')
  
  print('Num users: ' + str(len(users)))
  
  
  return users, ratings_export

def get_movies():
  """
  Returns list of movies from movie data
  """
  
  movie_data = pd.read_csv("movie_data.csv")
  movie_data = movie_data.drop(["imdb_id","imdb_link", "image_url", "tmdb_id", "tmdb_link"], axis = 1)
  
  movies = [movie for movie in movie_data['movie_id']]
  print('Num movies: ' + str(len(movies)))
  
  return movies
  
    

  
#download_data()
#get_data()
get_movies()