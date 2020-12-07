# document similarity API

## Table of Cotents
1. [Requirements](README.md#requirements)
2. [Directory tree structurer](README.md#directory-tree-structurer)
3. [Setup](README.md#setup)
4. [How to get the similarity score?](README.md#how-to-get-the-similarity-score)
5. [Testing](README.md#Testing)

## Requirements
- python3+

## directory tree structure
```sh
├── document_similarity_score
│   ├── __init__.py
│   ├── app.py
│   ├── document_similarity_score.py
│   ├── stop_words.py
│   ├── utils.py
│   └── README.md
├── requirements
│   ├── development.txt
│   ├── production.txt
│   └── testing.txt
├── tests
│   ├── __init__.py
│   ├── document_similarity_score_test.py
│   └── utils_test.py
└── requirements.txt
```

## Setup
- Install requirements
```sh
$ git clone git@github.com:LiamWahahaha/document-similarity-api.git
$ cd document-similarity-api
$ python3 -m venv venv
$ . venv/bin/activate
$ pip3 install -r requirements.txt
```

## How to get the similarity score?
  - Use it as a python library:
  ```
  from document_similarity_score.document_similarity_score import Context
  from document_similarity_score.document_similarity_score import StrategyJaccardIndex

  context = Context(StrategyJaccardIndex())
  
  document1 = "..."
  document2 = "..."
  similarity_score = context.calculate_document_similarity_score(document1, document2)
  print(f"The similarity score of document1 and document2 is ${similarity_score}")
  ```
  - for example:
  ```
  from document_similarity_score.document_similarity_score import Context
  from document_similarity_score.document_similarity_score import StrategyJaccardIndex

  context = Context(StrategyJaccardIndex())
  
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

## Testing
If you want to run the tests, you have to install additional modules first as follows
```sh
$ pip3 install -r requirements/development.txt
```
Then you can run the tests as follows
```sh
$ python3 -m unittest tests/* -v
```
