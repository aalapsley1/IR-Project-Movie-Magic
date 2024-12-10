import re

class Processor:
    def __init__(self):
        self.liked_movies = []
        self.disliked_movies = []
        self.genres = []
        self.keywords = []

    def tokenize(self, text):
        # Regex to find each attribute set within the localGPT output
        liked_movies_pattern = r"([\"'{\[]?liked[_\s]?movies[\"'}\]]?\s*[:=]\s*.*?\[.*?\])"
        disliked_movies_pattern = r"([\"'{\[]?disliked[_\s]?movies[\"'}\]]?\s*[:=]\s*.*?\[.*?\])"
        genres_pattern = r"([\"'{\[]?genres[\"'}\]]?\s*[:=]\s*.*?\[.*?\])"
        keywords_pattern = r"([\"'{\[]?keywords[\"'}\]]?\s*.*?\[:=]\s*.*?\[.*?\])"

        # Find matches in the localGPT out
        liked_movies_match = re.search(liked_movies_pattern, text, re.IGNORECASE)
        disliked_movies_match = re.search(disliked_movies_pattern, text, re.IGNORECASE)
        genres_match = re.search(genres_pattern, text, re.IGNORECASE)
        keywords_match = re.search(keywords_pattern, text, re.IGNORECASE)

        # Helper function
        def extract_list(match):
            if match:
                # Extract content within the brackets
                content = re.search(r"\[(.*?)\]", match.group(0))
                if content:
                    return [item.strip().strip('"') for item in content.group(1).split(",") if item.strip()]
            return []

        # Assign lists to respective variables
        self.liked_movies = extract_list(liked_movies_match)
        self.disliked_movies = extract_list(disliked_movies_match)
        self.genres = extract_list(genres_match)
        self.keywords = extract_list(keywords_match)


text = """
DBased on your provided context, here are the recommendations organized into the four distinct categories you requested: "Liked Movies": ["Inception", "The Shawshank Redemption", "The Dark Knight", "Interstellar", "Parasite", "Whiplash", "The Matrix", "The Godfather", "Spirited Away", "The Grand Budapest Hotel"] "Disliked Movies": ["Transformers: Age of Extinction", "Twilight", "The Room", "Cats", "Battlefield Earth", "Fifty Shades of Grey", "Sharknado"] "Genres": ["Sci-Fi", "Thriller", "Action", "Crime", "Drama", "Comedy", "Animation", "Fantasy", "Adventure", "Romance", "Musical"] "Keywords": ["amazing", "deeply moving", "thrilling", "captivating", "mind-blowing", "brilliantly crafted", "intensely inspiring", "groundbreaking", "masterpiece", "enchanting", "delightfully quirky", "tedious", "overblown", "overly dramatic", "unimpressive", "laughable", "unbearable", "terrible", "awkward", "engaging"]
"""

#init processor & tokenize example text
tokenizer = Processor()
tokenizer.tokenize(text)

# Output the parsed movie components
print("Liked Movies:", tokenizer.liked_movies)
print("Disliked Movies:", tokenizer.disliked_movies)
print("Genres:", tokenizer.genres)
print("Keywords:", tokenizer.keywords)
