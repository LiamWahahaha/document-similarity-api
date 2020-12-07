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


class StrategyJaccardIndex(Strategy):
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


class StrategyWordVector(Strategy):
    pass


class StrartegyTFIDF(Strategy):
    pass
