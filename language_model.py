import pandas as pd
from helper import *

# query to test language model
query = "flights to tokyo"

# get dataset from csv file
dataset = pd.read_csv('./flights_tickets_serp2020-04-01_cleaned.csv')

# preprocess the query
query = preprocess(query)

# get documents from dataset
documents = dataset['snippet'].tolist()

# convert each document into frequncy of words
documents = [preprocess(document) for document in documents]

# find probability of each word in query in each document
def get_probability(query, document):
    # get the count of each word in query in the document
    query_count = {}
    for word in query:
        # check how many times the word appears in the document
        count = document.count(word)
        # add the word and its count to the dictionary
        query_count[word] = count
    # get the total number of words in the document
    total_words = len(document)
    # get the probability of each word in the query
    probabilities = []
    for word in query:
        # get the probability of the word in the document
        probability = query_count[word] / total_words
        # add the probability to the list
        probabilities.append(probability)

    # get the probability of the query in the document
    probability = 1
    for probability in probabilities:
        probability *= probability

    return probability

def language_model(query, documents):
    probabilities = []
    for document in documents:
        probability = get_probability(query, document)
        probabilities.append({"probablity": probability, "doc_pos": documents.index(document)})

    # sort the probabilities in descending order
    probabilities.sort(key=lambda x: x['probablity'], reverse=True)

    # return title and link of top 10 documents
    return [{'title': dataset['title'][x['doc_pos']], 'link': dataset['link'][x['doc_pos']]} for x in probabilities[:10]]

# ranked_documents = language_model(query, documents)

# print(ranked_documents)
    

