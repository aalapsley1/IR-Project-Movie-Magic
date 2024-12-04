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
  
  movies_export = pd.read_csv("movie_data.csv")
  movies_export = movies_export.drop(["imdb_id","imdb_link", "image_url", "tmdb_id", "tmdb_link"], axis = 1)
  movies_export = movies_export[movies_export["year_released"].notna()]
  ratings_export = pd.read_csv("ratings_export.csv")
  users_export = pd.read_csv("users_export.csv")
  
  return movies_export, ratings_export, users_export
  
#download_data()
get_data()