# Design document
## Goal
Calculate the similarity score between two texts. If documents are exactly the
same, then the score should be 1. If the documents don't have any words in
common then the score should be 0.

## Considerations:
- Should I count punctuation or only words?
In the first version, I only count words. However, if there are no space between
the punctuation, I will treat it as a word. For example, I will treat
"you.got.me" as one word and "you got me!" will be "you", "got", "me".

- Which words should matter in the similarity comparison?
I use a set, stop_words, to store the common words that should not take into
account.

- Do you care about the ordering of words?
Sort of. I not only treat single word as a token but also treat it and its
neighbor as a token.

- What metric do I use to assign a numerical value to the similarity?
I use Jaccard distance to calculate the similarity score. Perhaps TF-IDF is
another way to try.

- What type of data structure should be used?

- Performance or accuracy?


## Questions behind the question
- What is this API for? Would this API be used for detecting idea similarity?

