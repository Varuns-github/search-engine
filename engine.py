from flask import Flask,jsonify,request

# define the app
app = Flask(__name__)

# dummy search results for now
initial_search_results = [
    { "id": "1", "title": "The Shawshank Redemption", "url": "https://www.imdb.com/title/tt0111161/" },
    { "id": "2", "title": "The Godfather", "url": "https://www.imdb.com/title/tt0068646/" },
    { "id": "3", "title": "The Godfather: Part II", "url": "https://www.imdb.com/title/tt0071562/" },
    { "id": "4", "title": "The Dark Knight", "url": "https://www.imdb.com/title/tt0468569/" },
];

# implement a list for caching results
cached_results = []

# endpoint to get the search results
@app.route("/search", methods=["GET"])
def get_search_results():
    # get the value of the query parameter
    query = request.args.get("query")

    print(query, "user inputted search query")
    # Pass the query to the retrieval models to get the search results

    # check if the query is in the cache
    for cache in cached_results:
        if cache["query"] == query:
            print("Found in cache")
            return jsonify(cache["results"])

    # update as dummy for now
    results = initial_search_results.copy()

    # update the cached results with the query and the search results
    cached_results.append({ "query": query, "results": results })

    return jsonify(results)

# endpoint to get which movie user selected
# This will be our evaluation endpoint
@app.route("/search/<query>", methods=["GET"])
def get_user_selected_search(query):

    user_input = request.args.get("selection")
    print(user_input, "User selected this movie")
    
    search_results = []

    # check if the query is in the cache
    for cache in cached_results:
        if cache["query"] == query:
            print("Found in cache")
            search_results = cache["results"]
            for result in search_results:
                # match the user selected movie with the search results
                if result["id"] == user_input:
                    # get the index of the selected movie
                    search_index = search_results.index(result)
                    # update the search results with the selected movie at the top
                    search_results.insert(0, search_results.pop(search_index))
                    
    # update the cached results with the query and the search results
    cached_results.append({ "query": query, "results": search_results })

    return jsonify(status="success", user_input=user_input)

app.run()
