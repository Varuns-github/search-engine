import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess(text):
    text = text.lower()
    text = " ".join(text.split())
    text = text.translate(str.maketrans('', '', string.punctuation))
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    filtered_text = [word for word in word_tokens if word not in stop_words]
    return filtered_text

def get_dataset(file_path):
    dataset = pd.read_csv(file_path)
    return dataset

def get_list_of_documents(dataset):
    documents = dataset['snippet'].tolist()
    documents = [preprocess(document) for document in documents]
    return documents
