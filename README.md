# search-engine
A very simple search engine with few IR models

We will use flask

In order to run, in your terminal run "python engine.py"

It has 2 endpoints for now both are GET, have not implemented POST or added any security feature

1. Endpoint to get the search results for a query

/search?query=<query>

Pass the user query as argument to this endpoint

2. Endpoint to return which result the user selected

http://127.0.0.1:5000/search/<query>?selection=<selected query id>