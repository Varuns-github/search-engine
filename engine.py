import time
from boolean_model import boolean_model
from language_model import language_model
from vector_space_model import vector_space_model
from cache import add_to_cache, get_cached_results
from evaluation import get_ground_truth, get_precision
from flask import Flask,jsonify,request,render_template
from helper import preprocess, get_dataset, get_list_of_documents

# define the app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# endpoint to get the search results
@app.route("/search", methods=["GET"])
def get_search_results():
    # get the value of the query parameter
    query = request.args.get("query")

    print(query, "user inputted search query")

    cache = get_cached_results(query)

    if(cache):
        return jsonify(cache)

    dataset = get_dataset('flights_tickets_serp2020-04-01_cleaned.csv')
    documents = get_list_of_documents(dataset)
    preprocessed_query = preprocess(query)

    ground_truth = get_ground_truth(query, dataset)

    # find the time taken to get the results from boolean model
    boolean_start_time = time.time()
    boolean_results = boolean_model(preprocessed_query, documents)
    boolean_end_time = time.time()
    boolean_precision = get_precision(ground_truth, boolean_results)

    # find the time taken to get the results from language model
    language_start_time = time.time()
    language_model_results = language_model(preprocessed_query, documents)
    language_end_time = time.time()
    language_precision = get_precision(ground_truth, language_model_results)

    # find the time taken to get the results from vector space model
    vector_start_time = time.time()
    vector_space_model_results = vector_space_model(preprocessed_query, documents)
    vector_end_time = time.time()
    vector_precision = get_precision(ground_truth, vector_space_model_results)

    # print the time taken to get the results
    print("Boolean model took", boolean_end_time - boolean_start_time, "seconds")
    print("Language model took", language_end_time - language_start_time, "seconds")
    print("Vector space model took", vector_end_time - vector_start_time, "seconds")

    # print the precision of the results
    print("Boolean model precision:", boolean_precision)
    print("Language model precision:", language_precision)
    print("Vector space model precision:", vector_precision)

    # check which model has the highest precision
    if(boolean_precision > language_precision and boolean_precision > vector_precision):
        print("Boolean model has the highest precision, returning results")
        results = boolean_results
    elif(language_precision > boolean_precision and language_precision > vector_precision):
        print("Language model has the highest precision, returning results")
        results = language_model_results
    else:
        print("Vector space model has the highest precision, returning results")
        results = vector_space_model_results

    # add the results to the cache
    add_to_cache(query, results)

    # return the results
    return jsonify(results)

# endpoint to get which website user selected
# This will be our evaluation endpoint
@app.route("/search/<query>", methods=["GET"])
def get_user_selected_search(query):

    user_input = request.args.get("selection")
    print(user_input, "User selected this website")
    
    cache = get_cached_results(query)

    if(cache):
        for result in cache:
            # match the user selected website with the search results
            if result["link"] == user_input:
                # get the index of the selected website
                search_index = cache.index(result)
                # update the search results with the selected website at the top
                cache.insert(0, cache.pop(search_index))
                    
    # update the cached results with the query and the search results
    add_to_cache(query, cache)

    return jsonify(status="success", user_input=user_input)

app.run()
