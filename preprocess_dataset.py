import pandas as pd
from helper import *

# read csv file
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

initial_dataset = read_csv('./flights_tickets_serp2020-04-01.csv')

# extract only the columns we need
def extract_columns(df):
    df = df[['searchTerms', 'title', 'snippet', 'link', 'rank']]
    return df

extracted_dataset = extract_columns(initial_dataset)

# remove rows with empty searchTerms
def remove_empty_searchTerms(df):
    df = df[df['searchTerms'].notnull()]
    return df

valid_dataset = remove_empty_searchTerms(extracted_dataset)

# get the first 10 rows of each unique searchTerms
def get_first_10_rows(df):
    df = df.groupby('searchTerms').head(10)
    return df

updated_dataset = get_first_10_rows(valid_dataset)

# display the dataset
print(updated_dataset.head())
print(updated_dataset.tail())

# number of unique searchTerms
print(updated_dataset['searchTerms'].nunique())

# highest rank
print(updated_dataset['rank'].max())

# maximum number of repated unique searchTerms
print(updated_dataset['searchTerms'].value_counts().max())

# preprocess the dataset for column searchTerms and snippet
def preprocess_dataset(df):
    df['searchTerms'] = df['searchTerms'].apply(preprocess)
    df['snippet'] = df['snippet'].apply(preprocess)
    return df

preprocessed_dataset = updated_dataset

# print df to a new csv file
preprocessed_dataset.to_csv('./flights_tickets_serp2020-04-01_cleaned.csv', index=False)

