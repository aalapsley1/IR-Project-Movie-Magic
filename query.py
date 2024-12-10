import pandas as pd
import math
import re

class Query:
    def __init__(self):
        self.movies = []  # List of all movies as tokenized lists
        self.genres = []  # List of genres as tokenized lists
        self.descriptions = []  # List of descriptions as tokenized lists
        self.genres_count = {}
        self.descriptions_count = {}
        self.genres_idf = {}  # IDF for genres
        self.keywords_idf = {}  # IDF for keywords
        self.scores = {}

    def tokenize(self, df):
        for index, row in df.iterrows():
            movie_entry = []
            for entry in row:
                clean_string = re.sub(r"[^a-z0-9 ]", " ", str(entry).lower())
                tokens = clean_string.split()
                movie_entry.append(tokens)
            self.movies.append(movie_entry)
        self.genres = [movie[1] for movie in self.movies]
        self.descriptions = [movie[4] for movie in self.movies]
            

    def compute_idf(self):
        num_docs = len(self.movies)

        # Compute document frequency for genres
        for genres in self.genres:
            unique = set(genres) # Count it once per entry 
            for genre in unique:
                if genre in self.genres_count:
                    self.genres_count[genre] += 1
                else:
                    self.genres_count[genre] = 1

        # Calculate IDF for genres
        for genre, count in self.genres_count.items():
            self.genres_idf[genre] = math.log(num_docs / count)

        # Compute document frequency for keywords (description words)
        for description in self.descriptions:
            unique = set(description) # count it once per doc
            for keyword in unique:
                if keyword in self.descriptions_count:
                    self.descriptions_count[keyword] += 1
                else:
                    self.descriptions_count[keyword] = 1

        # Calculate IDF for keywords
        for keyword, count in self.descriptions_count.items():
            self.keywords_idf[keyword] = math.log(num_docs / count) 

    def tf_idf(self, query_keywords, query_genres = ''):
        for i in range(len(self.movies)):
            movie = self.movies[i]
            genres = self.genres[i]
            description = self.descriptions[i]

            genre_score = 0
            keyword_score = 0

            for genre in query_genres:
                if genres != []:
                    if genres.count(genre):
                        tf = float(genres.count(genre)) / len(genres)
                        idf = self.genres_idf.get(genre)
                        genre_score += tf * idf

            for keyword in query_keywords:
                if description != []:
                    if description.count(keyword):
                        tf = float(description.count(keyword)) / len(description)
                        idf = self.keywords_idf.get(keyword) 
                        keyword_score += tf * idf

            title = "-".join(movie[2]) 
            self.scores[title] = (0.5 * genre_score) + (0.5 * keyword_score)

        return self.scores


    def query(self, keywords, genres):
        query_keywords = re.sub(r"[^a-z0-9 ]", " ", str(keywords).lower()).split()
        query_genres = re.sub(r"[^a-z0-9 ]", " ", str(genres).lower()).split()
        result = self.tf_idf(query_keywords, query_genres)
        sorted_result = sorted(result.items(), key=lambda x: -x[1])
        #print(sorted_result[:10])
        return result
    
    def data(self, movie_data):
        movie_data = movie_data.drop(
            [
                "image_url", "imdb_id", "imdb_link", "original_language", "popularity",
                "production_countries", "release_date", "runtime", "spoken_languages",
                "tmdb_id", "tmdb_link", "vote_average", "vote_count", "year_released"
            ], axis=1)
        return movie_data
    
    def run_query(self, data, keywords, genres):
        movie_data = self.data(data)
        self.tokenize(movie_data)
        self.compute_idf()
        results = self.query(keywords, genres)
        return results


# Main function
def main(args):
    q = Query()
    movie_data = pd.read_csv("movie_data.csv")
    result = q.run_query(movie_data, ["tehsadlt", "Football", "crazy", "football", "mad", "Don’t", "watch", "this", "off-beat", "jukebox", "cartoon", "expecting", "any", "conventional", "soccer", "action", "Equal", "parts", "Disney", "Dali", "and", "Duchamp", "this", "abstract", "mix", "of", "black", "and", "white", "photos", "and", "alternative", "comix", "style", "animation", "is", "accompanied", "by", "a", "medley", "of", "doo-wop", "classics",  "and", "documentary", "soundbites",  "The", "film", "is", "certainly", "an", "extreme", "departure", "for", "those", "familiar", "with", "the", "more", "conventional", "output", "of", "the", "Halas", "Batchelor", "studio", "best", "known", "for", "their", "feature-length", "version", "of", "George", "Orwell’s", "Animal", "Farm", "Paul", "Vester", "was", "one", "of", "a", "number", "of", "sixties", "art", "school", "graduates", "that", "brought", "a", "mix", "of", "pop", "art", "and", "illustration", "influences", "to", "the", "company", "whilst", "it", "was", "undergoing", "a", "brief", "change", "in", "its", "ownership", "As", "a", "warning", "in", "keeping", "with", "its", "progressive", "adult", "style", "there", "is", "some", "brief", "nudity", "at", "the", "end", "of", "the", "film"], ["Music", "animation"])
    print(result)


if __name__ == "__main__":
    import sys
    main(sys.argv)
