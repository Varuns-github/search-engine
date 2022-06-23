def get_ground_truth(query, documents):
    ground_truth = []
    # get index and document using loop
    for index, document in enumerate(documents['searchTerms']):
        # get searchTerm column from dataset
        if query in document:
            
            # get the title from documents with the same index
            ground_truth.append(documents['title'][index])

    return ground_truth

def get_precision(ground_truth, search_result):
    number_of_relavant_results = 0
    for result in search_result:
        if result['title'] in ground_truth:
            number_of_relavant_results += 1

    return number_of_relavant_results / 10
