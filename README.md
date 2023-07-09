# dedupeknn
dedupeknn is an innovative project designed to address the challenges of 
finding duplicated addresses and performing address matching efficiently. 
Leveraging advanced technologies such as FastText for generating 
vector representations and OpenSearch as a vector data source, 
Dedupeknn offers powerful solutions for these tasks. 
By employing nearest neighbor algorithms from NMSLIB, dedupeknn 
achieves accurate and speedy address comparisons.

dedupeknn utilizes the FastText library, renowned for its effectiveness 
in generating high-quality vector representations of text inputs. 
By transforming address strings into vector embeddings, dedupeknn 
captures the semantic meaning and contextual information essential 
for accurate address comparisons.

The OpenSearch framework serves as the vector data source for dedupeknn. 
OpenSearch is a search db maintained by AWS that provides efficient 
storage and retrieval capabilities for large-scale 
vector datasets. With OpenSearch, dedupeknn can handle vast amounts of 
address data, ensuring scalability and performance.

To find the nearest neighbors of a given address vector, 
Dedupeknn employs nearest neighbor algorithms from NMSLIB. 
These algorithms efficiently search the vector data source to 
identify the most similar addresses, allowing for effective 
deduplication and address matching.

By combining the strengths of FastText, OpenSearch, and NMSLIB, 
dedupeknn delivers a robust and accurate solution for addressing 
the challenges of duplicated addresses and address matching. 
Its fast and efficient algorithms enable organizations to streamline 
their operations, enhance data quality, and improve customer experiences.

## Running dedupeknn
1. The project uses `fastapi` library and runs as a microservice. The dependencies include
running opensearch cluster with _opensearch-knn_ plugin installed.
2. The configuration is loaded from the properties file - `properties/opensearch-client.properties` 
. Set the values accordingly with your installation setup.
3. Creating a new conda environment - `conda create -n dedupeknn python=3.10`
4. Install the required dependencies by - `pip install -r requirements.txt`
5. Run the project - `python main.py`

## Creating KNN index before ingesting data
The below example shows, how to create opensearch index with knn support.
```json
{
  "settings": {
    "index": {
      "knn": true,
      "knn.algo_param.ef_search": 100
    }
  },
  "mappings": {
    "properties": {
        "dedupe_vector_nmslib": {
          "type": "knn_vector",
          "dimension": 300,
          "method": {
            "name": "hnsw",
            "space_type": "cosinesimil",
            "engine": "nmslib",
            "parameters": {
              "ef_construction": 128,
              "m": 24
            }
          }
        }
    }
  }
}
```
Note:
1. We are using _consinesimil_ as KNN similarity match pattern.
2. Using KNN algorihm implementation from _nmslib_ (non-metric space library).
3. The fasttext model that we use for creating vector representation on input data is of 300 dimensions.
So, we set the field _dimensions_ value to 300. If you are using any other model with 500 or 800
dimensions, change this filed accordingly.

## API's exposed

### Ingesting data:
```shell
curl --location 'http://localhost:8080/api/v1/knn/doc/insert' \
--header 'Content-Type: application/json' \
--data '{
    "text": "#6/A Shashank J, 3rd Floor, Chetan Nilaya, 20 C Cross Rd, Ejipura, Bengaluru - 560047"
}'
```

### Getting vector representation of a string
```shell
curl --location 'http://localhost:8080/api/v1/vector/representation' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "*@) sdfd *29&3 -2030"
}'
```

### Getting K-Nearest-Neighbours for the input string
```shell
curl --location 'http://localhost:8080/api/v1/similarity/knn/search' \
--header 'Content-Type: application/json' \
--data '{
    "text": "Chetan Nilaya, House No 6, 3rd Floor, Ejipur, Bangalore 560047",
    "size": 30,
    "k": 1
}'
```
Note:
1. size - number of neighbours.
2. k - level of neighbours.

### Similarity Match
```shell
curl --location 'http://localhost:8080/api/v1/similarity/address/search' \
--header 'Content-Type: application/json' \
--data '{
    "text": "#6/A Third Floor, ChetanNilaya, 20C Road Ejipura,  bengaluru karnataka 560047",
    "size": 30,
    "k": 1,
    "threshold": 70
}'
```