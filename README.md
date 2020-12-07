# document similarity API

## Table of Cotents
- [Requirements](README.md#requirements)
- [Directory tree structure](README.md#directory-tree-structure)
- [Setup](README.md#setup)
- [How to get the similarity score?](README.md#how-to-get-the-similarity-score)
  - [Use it as a Python library](README.md#use-it-as-a-python-library)
  - [Via sending a POST request](README.md#via-sending-a-post-request)
    - [Test via cURL](README.md#test-via-curl)
    - [Test via NodeJS](README.md#test-via-nodejs)
    - [Test via Python](README.md#test-via-python)
- [Unit testing](README.md#unit-testing)
- [Misc](README.md#misc)

## Requirements
- python3+

## directory tree structure
```sh
├── document_similarity_score
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── document_similarity_score.py
│   ├── README.md
│   ├── stop_words.py
│   └── utils.py
├── requirements
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
├── tests
│   ├── __init__.py
│   ├── document_similarity_score_test.py
│   └── utils_test.py
├── Dockerfile
├── README.md
├── requirements.txt
└── wsgi.py
```
For the design document, please see 
## Setup
- Install requirements
```sh
$ git clone git@github.com:LiamWahahaha/document-similarity-api.git
or
$ git clone https://github.com/LiamWahahaha/document-similarity-api.git
$ cd document-similarity-api
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
```

## How to get the similarity score?
### Use it as a python library:
- Currently, there are two strategy options for calculating the similarity score:
  - ConcreteStrategyJaccardIndex
  - ConcreteStrategyWordVector
```
from document_similarity_score.document_similarity_score import Context
from document_similarity_score.document_similarity_score import ConcreteStrategyJaccardIndex

context = Context(ConcreteStrategyJaccardIndex())

document1 = "..."
document2 = "..."
similarity_score = context.calculate_document_similarity_score(document1, document2)
print(f"The similarity score of document1 and document2 is ${similarity_score}")
```
- for example:
```
from document_similarity_score.document_similarity_score import Context
from document_similarity_score.document_similarity_score import ConcreteStrategyJaccardIndex

context = Context(ConcreteStrategyJaccardIndex())

sample1 = """The easiest way to earn points with Fetch Rewards is to just shop for the products you
already love. If you have any participating brands on your receipt, you'll get points based on the 
cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each 
grocery receipt after you shop and we'll find the savings for you."""

sample2 = """The easiest way to earn points with Fetch Rewards is to just shop for the items you 
already buy. If you have any eligible brands on your receipt, you will get points based on the total 
cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your
receipt after you check out and we will find the savings for you."""

similarity_score = context.calculate_document_similarity_score(sample1, sample2)
print(f"The similarity score of sample1 and sample2 is ${similarity_score}")
```

### Via sending a POST request:
- approach 1, run the Flask application with the following command:
```sh
$ python3 wsgi.py
```
- approach 2, run the Docker image with the following command:
```sh
$ docker pull alphamonkey9/document-similarity-api:ver.2
$ docker run --rm -p 5001:5001 alphamonkey9/document-similarity-api:ver.2
```
or
```
$ docker pull alphamonkey9/document-similarity-api:word-vector
$ docker run --rm -p 5001:5001 alphamonkey9/document-similarity-api:word-vector
```
Once the server is running, you can test the API via many ways, such as:

#### Test via cURL
  
```
curl --location --request POST 'http://127.0.0.1:5001/similarity-score' \
--header 'Content-Type: application/json' \
--data-raw '{
    "document1": "The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'\''ll get points based on the cost of the products. You don'\''t need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'\''ll find the savings for you.",
    "document2": "The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you."
}'
```

#### Test via NodeJS
  
```
var axios = require('axios');
var data = JSON.stringify({"document1":"The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you.","document2":"The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you."});

var config = {
  method: 'post',
  url: 'http://127.0.0.1:5001/similarity-score',
  headers: { 
    'Content-Type': 'application/json'
  },
  data : data
};

axios(config)
.then(function (response) {
  console.log(JSON.stringify(response.data));
})
.catch(function (error) {
  console.log(error);
});
```

#### Test via Python
```
import http.client
import mimetypes
conn = http.client.HTTPSConnection("127.0.0.1", 5001)
payload = "{\n    \"document1\": \"The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you.\",\n    \"document2\": \"The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you.\"\n}"
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/similarity-score", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
```
or
```
import requests

url = "http://127.0.0.1:5001/similarity-score"

payload="{\n    \"document1\": \"The easiest way to earn points with Fetch Rewards is to just shop for the products you already love. If you have any participating brands on your receipt, you'll get points based on the cost of the products. You don't need to clip any coupons or scan individual barcodes. Just scan each grocery receipt after you shop and we'll find the savings for you.\",\n    \"document2\": \"The easiest way to earn points with Fetch Rewards is to just shop for the items you already buy. If you have any eligible brands on your receipt, you will get points based on the total cost of the products. You do not need to cut out any coupons or scan individual UPCs. Just scan your receipt after you check out and we will find the savings for you.\"\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

## Unit testing
If you want to run the tests, you have to install additional modules first as follows
```sh
$ pip3 install -r requirements/development.txt
```
Then you can run the tests as follows
```sh
$ python3 -m unittest tests/* -v
```

## Misc
- It would be great to use a Python code formatter to help formatting such as [black](#https://github.com/psf/black)
