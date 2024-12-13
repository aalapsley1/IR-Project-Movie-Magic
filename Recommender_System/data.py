import pandas as pd
import kagglehub

def download_data():

  '''
  Ok, I cannot figure out how to not have this download to a random location, 
  So it downloads to wherever it feels, and then prints out the location
  Find it, move the three files into this folder, and then get_data
  '''
  path = kagglehub.dataset_download("samlearner/letterboxd-movie-ratings-data")
  print("Path to dataset files:", path)

def get_data():
  """
  Loads and returns the data in panda dataframes.
  """
  
  movies_data = pd.read_csv("movie_data.csv")
  movies_data = movies_data.drop(["imdb_id","imdb_link", "image_url", "tmdb_id", "tmdb_link"], axis = 1)
  movies_data = movies_data[movies_data["year_released"].notna()]
  ratings_export = pd.read_csv("ratings_export.csv")
  users_export = pd.read_csv("users_export.csv")
  
  return movies_data, ratings_export, users_export

def get_users():
  
  """
  Returns list of users from ratings data
  """
  
  ratings_export = pd.read_csv("ratings_export.csv")
  
  '''
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
  '''
  
  user_dict = {}
  for a, row_data in ratings_export.iterrows():
    if row_data[3] not in user_dict.keys():
      user_dict[row_data[3]] = [(row_data[1], row_data[2])]
    else:
      user_dict[row_data[3]].append((row_data[1], row_data[2]))
  
  print(user_dict['deathproof'])
  
  return user_dict, ratings_export

def get_movies():
  """
  Returns list of movies from movie data
  """
  
  movie_data = pd.read_csv("movie_data.csv")
  movie_data = movie_data.drop(["imdb_id","imdb_link", "image_url", "tmdb_id", "tmdb_link"], axis = 1)
  
  movies = [movie for movie in movie_data['movie_id']]
  print('Num movies: ' + str(len(movies)))
  
  return movies

if __name__ == "__main__":
  download_data()
