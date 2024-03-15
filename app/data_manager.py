import os
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz, process
from scipy.spatial.distance import cdist

def load_data():
    filepath = os.getenv('DATA_FILEPATH')
    columns = ['name', 'alt_name', 'lat', 'long', 'country', 'admin1', 'population']
    df = pd.read_csv(filepath, sep='\t', usecols=columns)

    # break out alt_names to their own rows for search
    df['alt_names'] = df['alt_name'].str.split(',').apply(lambda x: x if isinstance(x, list) else [])
    df['all_names'] = df[['name', 'alt_names']].apply(lambda x: [x['name']] + x['alt_names'], axis=1)
    df['all_names'] = df['all_names'].apply(lambda x: list(set(x))) # remove duplicates
    df = df.explode('all_names').reset_index(drop=True)

    # remove cities irrelevant to the challenge
    filtered_df = df[(df['country'].isin(['US', 'CA'])) & (df['population'] > 5000)]

    return filtered_df

def calculate_scores(df, query, latitude=None, longitude=None, score_threshold=75):
    choices = df['all_names'].tolist()
    matches = process.extract(query, choices, limit=100, scorer=fuzz.token_sort_ratio)
    matches = [match for match in matches if match[1] >= score_threshold] # tune threshold to get more/less

    if not matches: # return empty
        return pd.DataFrame(columns=['name', 'admin1', 'country', 'lat', 'long', 'score'])

    matches_df = pd.DataFrame(matches, columns=['name', 'fuzzy_score'])
    matching_df = df.merge(matches_df, on='name')
    
    if latitude and longitude:
        matching_df['distance'] = cdist(
            matching_df[['lat', 'long']].astype(float),
            np.array([[float(latitude), float(longitude)]]),
            metric='euclidean'
        ).flatten()

        # normalize then invert, a lower distance is a higher score
        max_distance = matching_df['distance'].max()
        distance_score = 1 - (matching_df['distance'] / max_distance)
        
        matching_df['score'] = (matching_df['fuzzy_score'] / 100) * 0.5 + distance_score * 0.5
        matching_df.drop(columns=['distance'], inplace=True)
    else:
        matching_df['score'] = matching_df['fuzzy_score'] / 100 # 0 to 1

    # limit to 10 since an autocomplete menu is usually short
    matching_df = matching_df.sort_values('score', ascending=False).drop_duplicates(subset=['lat', 'long']).head(10)
    matching_df['score'] = matching_df['score'].apply(lambda x: round(x, 3)) # scores can be close but readable
    
    return matching_df[['name', 'admin1', 'country', 'lat', 'long', 'score']]
