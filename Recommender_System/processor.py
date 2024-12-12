import re

class Processor:
    def __init__(self):
        self.liked_movies = []
        self.disliked_movies = []
        self.genres = []
        self.keywords = []

    def getKeywords(self):
        return self.keywords
    
    def getGenres(self):
        return self.genres
    
    def recvQuery(self, text):
        self.parse_answer(text)
        self.tokenize(text)

    def parse_answer(self, answer):
        liked_movies_pattern = r'\"Liked Movies\": \[(.*?)\]'
        disliked_movies_pattern = r'\"Disliked Movies\": \[(.*?)\]'
        genres_pattern = r'\"Genres\": \[(.*?)\]'
        keywords_pattern = r'\"Keywords\": \[(.*?)\]'

        self.liked_movies = self.extract_items(answer, liked_movies_pattern)
        self.disliked_movies = self.extract_items(answer, disliked_movies_pattern)
        self.genres = self.extract_items(answer, genres_pattern)
        self.keywords = self.extract_items(answer, keywords_pattern)

    def extract_items(self, text, pattern):
        match = re.search(pattern, text)
        if match:
            items = match.group(1)
            return [item.strip().strip('"') for item in items.split(',')]
        return []

    def tokenize(self, text):
        # Implement your tokenize logic here
        pass

# # Example usage
# text = """
#   Sure, I'd be happy to help! Based on the user's query, here is the information I have gathered:\n["Liked Movies": ["Serotonin"], "Disliked Movies": ["Collateral Beauty"], "Genres": ["Comedy", "Drama"], "Keywords": ["feel-good"]]\nIt seems that the user likes the movie "Serotonin" and wants a similar feel-good movie. However, they did not enjoy "Collateral Beauty". The genres associated with this query are "Comedy" and "Drama", as those are the genres of the movies mentioned in the query. The keywords extracted from the query are "feel-good".
#   """

# # init processor & parse example text
# processor = Processor()
# processor.recvQuery(text)

# # Output the parsed movie components
# print("Liked Movies:", processor.liked_movies)
# print("Disliked Movies:", processor.disliked_movies)
# print("Genres:", processor.genres)
# print("Keywords:", processor.keywords)