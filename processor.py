def tokenize(text):
  """
  Converts the text into keywords, movies, and actors.
  (Eventually) uses mini-gpt to process the user input text. 
  
  Parameters:
    text:
      Raw user query.
      Example: "A thrilling movie that has Morgan Freeman and is similar to The Dark Knight."
    
  Returns: 
    keywords:
      A list of keywords to query by.
      Example: ['Thriller']
    movies:
      A list of movies to recommend by.
      Example: ['The Dark Knight']
    actors:
      A list of actors to recommend by.
      Example: ['Morgan Freeman']
  """