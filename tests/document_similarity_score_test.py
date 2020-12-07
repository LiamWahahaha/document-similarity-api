import unittest

from document_similarity_score.utils import TextProcessor as processor
from document_similarity_score.document_similarity_score import (
    ConcreteStrategyJaccardIndex,
    ConcreteStrategyWordVector,
)


class ConcreteStrategyJaccardIndexTest(unittest.TestCase):
    def test_calculate_jaccard_index(self):
        calculate_jaccard_index = ConcreteStrategyJaccardIndex().calculate_jaccard_index

        set1 = set([1, 2, 3])
        set2 = set([1, 2, 3])
        self.assertEqual(calculate_jaccard_index(set1, set2), 1)

        set1 = set([1, 2])
        set2 = set([1, 2, 3])
        self.assertAlmostEqual(calculate_jaccard_index(set1, set2), 2 / 3)

    def test_calculate_similarity_score(self):
        calculate_similarity_score = (
            ConcreteStrategyJaccardIndex().calculate_similarity_score
        )
        weighting = ConcreteStrategyJaccardIndex().weighting

        text1 = "abc"
        text2 = "abc"
        self.assertEqual(calculate_similarity_score(text1, text2), 1)

        text1 = "abc"
        text2 = "Abc"
        self.assertEqual(calculate_similarity_score(text1, text2), 0.99)

        text1 = "abc"
        text2 = "Abc!"
        self.assertEqual(calculate_similarity_score(text1, text2), 0.99)

        text1 = "a b c"
        text2 = "a b"
        expected1 = weighting * 3 / 5
        expected2 = weighting * 2 / 4
        self.assertAlmostEqual(
            calculate_similarity_score(text1, text2, False), expected1
        )
        self.assertAlmostEqual(
            calculate_similarity_score(text1, text2, True), expected2
        )


class ConcreteStrategyWordVectorTest(unittest.TestCase):
    def test_calculate_cosine_similarity(self):
        calculate_cosine_similarity = (
            ConcreteStrategyWordVector().calculate_cosine_similarity
        )

        p1 = processor("c d")
        p2 = processor("c d")
        corpus_domain = processor.get_corpus_domain(
            [p1.token_counter, p2.token_counter]
        )
        vector1 = processor.get_word_vector(p1.token_counter, corpus_domain)
        vector2 = processor.get_word_vector(p2.token_counter, corpus_domain)
        self.assertAlmostEqual(calculate_cosine_similarity(vector1, vector2), 1)

        p1 = processor("c c d")
        p2 = processor("c c c c d")
        corpus_domain = processor.get_corpus_domain(
            [p1.token_counter, p2.token_counter]
        )
        vector1 = processor.get_word_vector(p1.token_counter, corpus_domain)
        vector2 = processor.get_word_vector(p2.token_counter, corpus_domain)
        expected = 13 / (7 ** 0.5) / (27 ** 0.5)
        self.assertAlmostEqual(calculate_cosine_similarity(vector1, vector2), expected)

    def test_calculate_similarity_score(self):
        calculate_similarity_score = (
            ConcreteStrategyWordVector().calculate_similarity_score
        )
        weighting = ConcreteStrategyWordVector().weighting

        text1 = "abc"
        text2 = "abc"
        self.assertEqual(calculate_similarity_score(text1, text2), 1)

        text1 = "abc"
        text2 = "Abc"
        self.assertEqual(calculate_similarity_score(text1, text2), 0.99)

        text1 = "abc"
        text2 = "Abc!"
        self.assertEqual(calculate_similarity_score(text1, text2), 0.99)

        text1 = "a b c"
        text2 = "a b"
        expected1 = weighting * 3 / (5 ** 0.5) / (3 ** 0.5)
        expected2 = weighting * 2 / (4 ** 0.5) / (2 ** 0.5)
        self.assertAlmostEqual(
            calculate_similarity_score(text1, text2, False), expected1
        )
        self.assertAlmostEqual(
            calculate_similarity_score(text1, text2, True), expected2
        )


if __name__ == "__main__":
    unittest.main()
