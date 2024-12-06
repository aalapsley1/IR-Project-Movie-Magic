import re

class Processor:
    def __init__(self):
        self.liked_movies = []
        self.disliked_movies = []
        self.genres = []
        self.keywords = []

    def tokenize(self, text):
        # Regex to find each attribute set within the localGPT output
        liked_movies_pattern = r"(liked[_\s]?movies\s*[:=]\s*\[.*?\])"
        disliked_movies_pattern = r"(disliked[_\s]?movies\s*[:=]\s*\[.*?\])"
        genres_pattern = r"(genres\s*[:=]\s*\[.*?\])"
        keywords_pattern = r"(keywords\s*[:=]\s*\[.*?\])"

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
User: Based on the query I am about to give you, please separate parts of the query into multiple sets (sets can be empty). First is liked movies, second is disliked movies, third is genres (if the adjective is not a movie genre like "humorous", translate to a real movie genre that is the closest synonymically). Fourth are keywords, these are the adjectives (as is) in the query. The items can be placed into the group sets like this [a] surrounded by brackets and with multiple entries within the brackets being separated by a comma. Here is the query "Recommend me a feel-good movie like Serotonin, but I didn't enjoy Collateral Beauty." ```python liked_movies = ["Serotonin"] disliked_movies = ["Collateral Beauty"] genres = [] keywords = ["feel-good"] [a] = liked_movies, disliked_movies, genres, keywords ```
"""

#init processor & tokenize example text
tokenizer = Processor()
tokenizer.tokenize(text)

# Output the parsed movie components
print("Liked Movies:", tokenizer.liked_movies)
print("Disliked Movies:", tokenizer.disliked_movies)
print("Genres:", tokenizer.genres)
print("Keywords:", tokenizer.keywords)
