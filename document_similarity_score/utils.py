from collections import defaultdict
from typing import Dict, List, Set
from string import punctuation

from document_similarity_score.stop_words import stop_words


class TextProcessor:
    def __init__(self, text: str = "") -> None:
        self.__normalized_text = self.normalize_text(text)
        self.__generate_default_token_counter()

    @property
    def normalized_text(self):
        return self.__normalized_text

    @normalized_text.setter
    def normalized_text(self, text: str):
        self.__normalized_text = self.normalize_text(text)
        self.__generate_default_token_counter()

    @property
    def token_counter(self):
        return self.__token_counter

    def __generate_default_token_counter(self):
        token_counter1 = self.get_token_counter(self.normalized_text)
        token_counter2 = self.get_token_counter(self.normalized_text, 2)
        self.__token_counter = self.merge_token_counters(token_counter1, token_counter2)

    @staticmethod
    def merge_token_counters(
        token_counter1: Dict[str, int], token_counter2: Dict[str, int]
    ) -> Dict[str, int]:
        for token, number in token_counter2.items():
            if token in token_counter1:
                token_counter1[token] += number
            else:
                token_counter1[token] = number

        return token_counter1

    @staticmethod
    def normalize_text(text: str) -> List[str]:
        normalized_text = []

        for word in text.split():
            preprocessed_word = TextProcessor.remove_punctuation(word)
            if preprocessed_word:
                normalized_text.append(preprocessed_word.lower())

        return normalized_text

    @staticmethod
    def remove_punctuation(word: str) -> str:
        """
        ver. 1: remove punctuation at the start and the end of each word
        but not the middle
        alternatives: keep the special cases, such as
            - super!!! -> super!!!
            - um?! -> um?!
        """
        return word.strip(punctuation)

    @staticmethod
    def get_token_counter(words: List[str], ngram: int = 1) -> Dict[str, int]:
        if ngram < 1:
            ngram = 1

        token_counter = defaultdict(int)

        for idx in range(0, len(words) - ngram + 1):
            word = " ".join(words[idx : (idx + ngram)])
            token_counter[word] += 1

        return token_counter

    @staticmethod
    def get_corpus_domain(
        token_counters: List[Dict[str, int]],
        without_stop_words: bool = True,
    ) -> Dict[str, int]:
        if not token_counters:
            raise ValueError("empty token counter")

        token_set = set()

        for token_counter in token_counters:
            token_set = token_set.union(set(token_counter.keys()))

        if without_stop_words:
            token_set = token_set.difference(stop_words)

        sorted_token_list = list(token_set)
        domain = {token: idx for idx, token in enumerate(sorted(sorted_token_list))}

        return domain

    @staticmethod
    def get_word_vector(
        token_counter: Dict[str, int], domain: Dict[str, int]
    ) -> List[int]:
        word_vector = [0] * len(domain)
        for token, number in token_counter.items():
            word_vector[domain[token]] = number

        return word_vector

    @staticmethod
    def remove_stop_words(
        token_counter: Dict[str, int], words: Set[str] = None
    ) -> Dict[str, int]:
        if words is None:
            words = stop_words

        return set(token_counter.keys()).difference(words)
