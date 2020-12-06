import unittest

from document_similarity_score.utils import TextProcessor as processor


class TextProcessorTest(unittest.TestCase):
    def test_remove_punctuation(self):
        remove_punctuation = processor.remove_punctuation

        self.assertEqual(remove_punctuation("Super!"), "Super")
        self.assertEqual(remove_punctuation("Super!!!"), "Super")
        self.assertEqual(remove_punctuation(":)"), "")
        self.assertEqual(remove_punctuation("3.5"), "3.5")
        self.assertEqual(remove_punctuation("Super!"), "Super")
        self.assertEqual(remove_punctuation("(for"), "for")
        self.assertEqual(remove_punctuation("example),"), "example")
        self.assertEqual(remove_punctuation("!!!example),"), "example")

    def test_merge_token_counter(self):
        p = processor()
        private_function = p.merge_token_counters

        token_1 = {"john": 1, "jane": 1}
        token_2 = {"john doe": 1, "jane doe": 1}
        expected = {"john": 1, "jane": 1, "john doe": 1, "jane doe": 1}
        self.assertEqual(private_function(token_1, token_2), expected)

    def test_normalize_text(self):
        normalize_text = processor.normalize_text

        text = "Function names start with verb do_something ()"
        expected = ["function", "names", "start", "with", "verb", "do_something"]
        self.assertEqual(normalize_text(text), expected)

        p = processor(text)
        self.assertEqual(p.normalized_text, expected)

        p.normalized_text = "@property decorator is a built-in decorator in Python"
        expected = [
            "property",
            "decorator",
            "is",
            "a",
            "built-in",
            "decorator",
            "in",
            "python",
        ]
        self.assertEqual(p.normalized_text, expected)

    def test_get_token_counter(self):
        get_token_counter = processor.get_token_counter
        normalize_text = processor.normalize_text

        text = "Function names start with verb do_something ()"
        expected = {
            "function": 1,
            "names": 1,
            "start": 1,
            "with": 1,
            "verb": 1,
            "do_something": 1,
        }
        self.assertEqual(get_token_counter(normalize_text(text)), expected)

        expected2 = {
            "function names": 1,
            "names start": 1,
            "start with": 1,
            "with verb": 1,
            "verb do_something": 1,
        }
        self.assertEqual(get_token_counter(normalize_text(text), 2), expected2)

    def test_default_token_counter(self):
        text = "Function names start with verb do_something ()"
        expected = {
            "function": 1,
            "names": 1,
            "start": 1,
            "with": 1,
            "verb": 1,
            "do_something": 1,
            "function names": 1,
            "names start": 1,
            "start with": 1,
            "with verb": 1,
            "verb do_something": 1,
        }
        p = processor(text)
        self.assertEqual(p.token_counter, expected)

    def test_get_corpus_domain(self):
        text1 = "Function names start with verb do_something ()"
        text2 = "Welcome to StackOverflow! Thanks for posting your code,"
        p1 = processor(text1)
        p2 = processor(text2)
        actual = processor.get_corpus_domain([p1.token_counter, p2.token_counter])
        expected = sorted(
            [
                "function",
                "names",
                "start",
                "verb",
                "do_something",
                "welcome",
                "stackoverflow",
                "thanks",
                "posting",
                "code",
                "function names",
                "names start",
                "start with",
                "with verb",
                "verb do_something",
                "welcome to",
                "to stackoverflow",
                "stackoverflow thanks",
                "thanks for",
                "for posting",
                "posting your",
                "your code",
            ]
        )
        expected = {token: idx for idx, token in enumerate(sorted(expected))}
        self.assertEqual(actual, expected)

    def test_get_word_vector(self):
        text1 = "b c r"
        text2 = "c b e f"
        p1 = processor(text1)
        p2 = processor(text2)
        domain = processor.get_corpus_domain([p1.token_counter, p2.token_counter])
        actual1 = processor.get_word_vector(p1.token_counter, domain)
        actual2 = processor.get_word_vector(p2.token_counter, domain)
        # domain:  b, bc, be, c, cb, cr, e, ef, f, r
        expected1 = [1, 1, 0, 1, 0, 1, 0, 0, 0, 1]
        expected2 = [1, 0, 1, 1, 1, 0, 1, 1, 1, 0]
        self.assertEqual(actual1, expected1)
        self.assertEqual(actual2, expected2)

    def test_remove_stop_words(self):
        text1 = "a b c"
        p1 = processor(text1)
        expected = set(["a b", "b c", "b", "c"])
        self.assertEqual(p1.remove_stop_words(p1.token_counter), expected)


if __name__ == "__main__":
    unittest.main()
