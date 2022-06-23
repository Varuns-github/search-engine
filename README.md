# search-engine

A search engine with three IR models: Boolean, Language and Vector Space model

We will use flask

In order to run the application, in your terminal run "python engine.py" and open "http://127.0.0.1:5000/" in the browser

It has 2 endpoints for now both are GET

1. Endpoint to get the search results for a query

    /search?query=[query]

    Pass the user query as argument to this endpoint

2. Endpoint to return which result the user selected

    /search/[query]?selection=[selected link]

    Pass the query as well as the selected link

We have cache implemented so if the same query is made again, the data will be returned from cache.

We calculate the precision for each model and the one with maximum precision is returned as the result.

Based on users selection we will re-order the search result to move the selection to the top.
The next time the same query is made the result is shown based on what the previous use selected.

Dataset used is https://www.kaggle.com/datasets/eliasdabbas/search-engine-results-flights-tickets-keywords