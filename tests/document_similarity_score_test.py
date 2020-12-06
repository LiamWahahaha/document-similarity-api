import unittest

from document_similarity_score.document_similarity_score import StrategyJaccardIndex


class StrategyJaccardIndexTest(unittest.TestCase):
    def test_calculate_jaccard_index(self):
        calculate_jaccard_index = StrategyJaccardIndex().calculate_jaccard_index

        set1 = set([1, 2, 3])
        set2 = set([1, 2, 3])
        self.assertEqual(calculate_jaccard_index(set1, set2), 1)

        set1 = set([1, 2])
        set2 = set([1, 2, 3])
        self.assertEqual(calculate_jaccard_index(set1, set2), 2 / 3)

    def test_calculate_similarity_score(self):
        calculate_similarity_score = StrategyJaccardIndex().calculate_similarity_score
        weighting = StrategyJaccardIndex().weighting

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
        self.assertEqual(calculate_similarity_score(text1, text2, False), expected1)
        self.assertEqual(calculate_similarity_score(text1, text2, True), expected2)


if __name__ == "__main__":
    unittest.main()
