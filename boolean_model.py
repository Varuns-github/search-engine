import pandas as pd
from helper import *

# Query to test boolean model
query = "flights to tokyo"

# Get dataset from csv file
dataset = pd.read_csv('./flights_tickets_serp2020-04-01_cleaned.csv')

# get documents from dataset
documents = dataset['snippet'].tolist()

# preprocess the query
query = preprocess(query)

# convert documents from class string to class list
documents = [preprocess(document) for document in documents]

def boolean_model(query, documents):
    weights = []
    query = ' '.join(query)
    for i in range(len(documents)):
        if query in ' '.join(documents[i]):
            weights.append({'weight': 1, 'doc_pos': i})
        else:
            weights.append({'weight': 0, 'doc_pos': i})

    # sort the weights in descending order
    weights.sort(key=lambda x: x['weight'], reverse=True)

    # return title and link of top 10 documents
    return [{'title': dataset['title'][x['doc_pos']], 'link': dataset['link'][x['doc_pos']]} for x in weights[:10]]

# ranked_documents = boolean_model(query, documents)

# print(ranked_documents)