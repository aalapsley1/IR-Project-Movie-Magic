import pandas as pd
import pickle
from tqdm import tqdm

# Paths to your CSV and output Pickle file
CSV_PATH = 'movie_metadata.csv'
PICKLE_PATH = 'metadata.pkl'

# Load CSV
df = pd.read_csv(CSV_PATH)

# Enable progress bar for DataFrame operations
tqdm.pandas(desc="Processing metadata")

# Helper function to safely evaluate JSON-like strings
def safe_eval(value):
    try:
        if isinstance(value, str):
            return eval(value)  # Converts stringified lists to actual lists
        return value  # If it's already a list or None, return as-is
    except Exception as e:
        print(f"Error evaluating value: {value}, Error: {e}")
        return None  # Return None for invalid entries

# Apply safe evaluation to relevant columns
df['genres'] = df['genres'].progress_apply(safe_eval)
df['production_countries'] = df['production_countries'].progress_apply(safe_eval)
df['spoken_languages'] = df['spoken_languages'].progress_apply(safe_eval)

# Convert the DataFrame to a list of dictionaries
metadata = df.to_dict(orient='records')

# Save as a Pickle file
with open(PICKLE_PATH, 'wb') as f:
    pickle.dump(metadata, f)

print(f"Metadata saved to {PICKLE_PATH}")
