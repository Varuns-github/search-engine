import pandas as pd
from helper import *
from gensim.models import Word2Vec
import numpy as np

query = "flights to hong kong"

# get dataset from csv file
dataset = pd.read_csv('./flights_tickets_serp2020-04-01_cleaned.csv')

# preprocess the query
query = preprocess(query)

# get documents from dataset
documents = dataset['snippet'].tolist()

# convert each document into frequncy of words
documents = [preprocess(document) for document in documents]

w2v_model = Word2Vec(documents, min_count=1,window=5, sg=1,workers=4)

def get_vector(query):
    embedding = []
    for word in query:
        try:
            embedding.append(w2v_model.wv.get_vector(word))
        except:
            embedding.append(w2v_model['unk'])
    return np.mean(embedding, axis=0)

def get_cosine_similarity(query, document):
    # get the vector representation of the query
    query_vector = get_vector(query)
    # print(query_vector)
    # get the vector representation of the document
    document_vector = get_vector(document)
    # finding cosine similarity between the two vectors
    cosine_similarity = np.dot(query_vector, document_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(document_vector))
    return cosine_similarity

def vector_space_model(query, documents):
    similarity = []
    for document in documents:
        # get cosine similarity of the query and the document
        cosine_similarity = get_cosine_similarity(query, document)
        similarity.append({"cosine_similarity": cosine_similarity, "doc_pos": documents.index(document)})

    # sort the probabilities in descending order
    similarity = sorted(similarity, key=lambda k: k['cosine_similarity'], reverse=True)

    return [{'title': dataset['title'][x['doc_pos']], 'link': dataset['link'][x['doc_pos']]} for x in similarity[:10]]

# ranked_documents = vector_space_model(query, documents)

# print(ranked_documents)