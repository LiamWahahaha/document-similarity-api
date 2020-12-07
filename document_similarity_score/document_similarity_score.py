from __future__ import annotations
from abc import ABC, abstractmethod

from .utils import TextProcessor


class Context:
    def __init__(self, strategy: Strategy) -> None:
        self.__strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self.__strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self.__strategy = strategy

    def calculate_document_similarity_score(self, text1: str, text2: str) -> float:
        similarity_score = self.__strategy.calculate_similarity_score(text1, text2)
        return similarity_score


class Strategy(ABC):
    @abstractmethod
    def calculate_similarity_score(self, text1: str, text2: str) -> float:
        pass


class ConcreteStrategyJaccardIndex(Strategy):
    weighting = 0.98

    def calculate_similarity_score(
        self, text1: str, text2: str, remove_stop_words: bool = True
    ) -> float:
        if text1 == text2:
            return 1.0

        tp1 = TextProcessor(text1)
        tp2 = TextProcessor(text2)

        if tp1.normalized_text == tp2.normalized_text:
            return 0.99

        token_set1 = (
            TextProcessor.remove_stop_words(tp1.token_counter)
            if remove_stop_words
            else set(tp1.token_counter.keys())
        )
        token_set2 = (
            TextProcessor.remove_stop_words(tp2.token_counter)
            if remove_stop_words
            else set(tp2.token_counter.keys())
        )
        return self.weighting * self.calculate_jaccard_index(token_set1, token_set2)

    def calculate_jaccard_index(self, set1: set, set2: set) -> float:
        """
        https://en.wikipedia.org/wiki/Jaccard_index
        """
        intersection_set = set1.intersection(set2)
        union_set = set1.union(set2)
        jaccard_index = 0

        try:
            jaccard_index = len(intersection_set) / len(union_set)
        except ZeroDivisionError:
            jaccard_index = 1

        return jaccard_index


class ConcreteStrategyWordVector(Strategy):
    weighting = 0.98

    def calculate_similarity_score(
        self, text1: str, text2: str, remove_stop_words: bool = True
    ) -> float:
        if text1 == text2:
            return 1.0

        tp1 = TextProcessor(text1)
        tp2 = TextProcessor(text2)

        if tp1.normalized_text == tp2.normalized_text:
            return 0.99

        corpus_domain = TextProcessor.get_corpus_domain(
            [tp1.token_counter, tp2.token_counter], remove_stop_words
        )
        word_vector1 = TextProcessor.get_word_vector(tp1.token_counter, corpus_domain)
        word_vector2 = TextProcessor.get_word_vector(tp2.token_counter, corpus_domain)
        return self.weighting * self.calculate_cosine_similarity(
            word_vector1, word_vector2
        )

    def calculate_cosine_similarity(
        self, word_vector1: List[int], word_vector2: List[int]
    ) -> float:
        inner_product = sum(
            [
                amplitude1 * amplitude2
                for amplitude1, amplitude2 in zip(word_vector1, word_vector2)
            ]
        )
        length_of_v1 = sum(map(lambda x: x ** 2, word_vector1))
        length_of_v2 = sum(map(lambda x: x ** 2, word_vector2))

        try:
            return (inner_product ** 2 / (length_of_v1 * length_of_v2)) ** 0.5
        except ZeroDivisionError:
            return 0


class ConcreteStrartegyTFIDF(Strategy):
    pass
