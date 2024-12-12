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
        # Go through lines of csv
        for index, row in df.iterrows():
            # initialize movie entry
            movie_entry = []
            # Go through each entry in the row (id, title, movie id, genres, description)
            for entry in row:
                # clean and tokenize each entry
                clean_string = re.sub(r"[^a-z0-9 ]", " ", str(entry).lower())
                tokens = clean_string.split()
                # add to movie entry 
                movie_entry.append(tokens)
            # save movie_entry 
            self.movies.append(movie_entry)
        # save genres and description 
        self.genres = [movie[1] for movie in self.movies]
        self.descriptions = [movie[4] for movie in self.movies]
            

    def compute_idf(self):
        num_docs = len(self.movies)

        # Compute document frequency for genres
        for genres in self.genres:
            # Count it once per entry
            unique = set(genres) 
            # count of how many times genre comes up in whole corpus
            for genre in unique:
                if genre in self.genres_count:
                    self.genres_count[genre] += 1
                else:
                    self.genres_count[genre] = 1

        # Calculate IDF for genres and saves it to dict
        for genre, count in self.genres_count.items():
            self.genres_idf[genre] = math.log(num_docs / count)

        # Compute document frequency for keywords (description words)
        for description in self.descriptions:
            # count it once per doc
            unique = set(description)
            # Count of how many times keyword comes up in whole corpus
            for keyword in unique:
                if keyword in self.descriptions_count:
                    self.descriptions_count[keyword] += 1
                else:
                    self.descriptions_count[keyword] = 1

        # Calculate IDF for keywords amd saves it
        for keyword, count in self.descriptions_count.items():
            self.keywords_idf[keyword] = math.log(num_docs / count) 

    def tf_idf(self, query_keywords, query_genres = ''):
        # for each movie 
        for i in range(len(self.movies)):
            # lists stay in the same order so movies[1] matches up with genres[1] and description[1]
            movie = self.movies[i]
            genres = self.genres[i]
            description = self.descriptions[i]

            # intitalize scores
            genre_score = 0
            keyword_score = 0

            # calculate tf-idf for each genre in the query
            for genre in query_genres:
                if genres != []:
                    if genres.count(genre):
                        tf = float(genres.count(genre)) / len(genres)
                        idf = self.genres_idf.get(genre)
                        genre_score += tf * idf

            # calculate tf-idf for each keyword in the query
            for keyword in query_keywords:
                if description != []:
                    if description.count(keyword):
                        tf = float(description.count(keyword)) / len(description)
                        idf = self.keywords_idf.get(keyword) 
                        keyword_score += tf * idf

            # make movie id again (it gets stripped of "-" in the tokenization process)
            title = "-".join(movie[2]) 
            # save movie id with score
            self.scores[title] = (0.5 * genre_score) + (0.5 * keyword_score)

        return self.scores


    def query(self, keywords, genres):
        # Clean keywords and genres
        query_keywords = re.sub(r"[^a-z0-9 ]", " ", str(keywords).lower()).split()
        query_genres = re.sub(r"[^a-z0-9 ]", " ", str(genres).lower()).split()
        # calcluates all tf-idf
        result = self.tf_idf(query_keywords, query_genres)
        # Sorts results 
        sorted_result = sorted(result.items(), key=lambda x: -x[1])
        # Finds max value
        max = sorted_result[0][1]
        #print(max)
        # normalized to -1 to 1
        for a in result:
            result[a] = (result[a]/max) * 2 - 1
        #print(sorted_result[:10])
        return result
    
    def data(self, movie_data):
        # clean dataset 
        movie_data = movie_data.drop(
            [
                "image_url", "imdb_id", "imdb_link", "original_language", "popularity",
                "production_countries", "release_date", "runtime", "spoken_languages",
                "tmdb_id", "tmdb_link", "vote_average", "vote_count", "year_released"
            ], axis=1)
        return movie_data
    
    def run_query(self, data, keywords, genres):
        # clean dataset
        movie_data = self.data(data)
        # tokenize dataset (and saves different lists)
        self.tokenize(movie_data)
        # compute idfs
        self.compute_idf()
        # get results
        results = self.query(keywords, genres)
        return results


# Main function
def main(args):
    # initialize object
    q = Query()
    # read data
    movie_data = pd.read_csv("movie_data.csv")
    # Compute results
    result = q.run_query(movie_data, ["tehsadlt", "Football", "crazy", "football", "mad", "Don’t", "watch", "this", "off-beat", "jukebox", "cartoon", "expecting", "any", "conventional", "soccer", "action", "Equal", "parts", "Disney", "Dali", "and", "Duchamp", "this", "abstract", "mix", "of", "black", "and", "white", "photos", "and", "alternative", "comix", "style", "animation", "is", "accompanied", "by", "a", "medley", "of", "doo-wop", "classics",  "and", "documentary", "soundbites",  "The", "film", "is", "certainly", "an", "extreme", "departure", "for", "those", "familiar", "with", "the", "more", "conventional", "output", "of", "the", "Halas", "Batchelor", "studio", "best", "known", "for", "their", "feature-length", "version", "of", "George", "Orwell’s", "Animal", "Farm", "Paul", "Vester", "was", "one", "of", "a", "number", "of", "sixties", "art", "school", "graduates", "that", "brought", "a", "mix", "of", "pop", "art", "and", "illustration", "influences", "to", "the", "company", "whilst", "it", "was", "undergoing", "a", "brief", "change", "in", "its", "ownership", "As", "a", "warning", "in", "keeping", "with", "its", "progressive", "adult", "style", "there", "is", "some", "brief", "nudity", "at", "the", "end", "of", "the", "film"], ["Music", "animation"])
    #print(result)
    return result


if __name__ == "__main__":
    import sys
    main(sys.argv)
