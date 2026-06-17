import unittest
from textkit import (
    parse_kv, slugify, truncate, normalize_ws, word_count, title_case,
)


class TestParseKV(unittest.TestCase):  # T1 target — 5 tests
    def test_basic(self):
        self.assertEqual(parse_kv("a: 1\nb: 2"), {"a": "1", "b": "2"})

    def test_value_with_colon(self):
        self.assertEqual(parse_kv("url: http://x"), {"url": "http://x"})

    def test_blank_lines_ignored(self):
        self.assertEqual(parse_kv("a: 1\n\nb: 2"), {"a": "1", "b": "2"})

    def test_comments_ignored(self):
        self.assertEqual(parse_kv("# comment\na: 1"), {"a": "1"})

    def test_whitespace_stripped(self):
        self.assertEqual(parse_kv("  a  :  1 "), {"a": "1"})


class TestSlugify(unittest.TestCase):  # T2 target — 3 tests
    def test_lowercase_and_hyphen(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_collapse_and_trim(self):
        self.assertEqual(slugify("  Multiple   Spaces  "), "multiple-spaces")

    def test_strip_punctuation(self):
        self.assertEqual(slugify("Foo!Bar?"), "foo-bar")


class TestTruncate(unittest.TestCase):  # T3 target — 2 failing + 1 control
    def test_truncates_to_length(self):
        self.assertEqual(truncate("hello world", 8), "hello w…")

    def test_truncates_and_rstrips(self):
        self.assertEqual(truncate("hello world", 6), "hello…")

    def test_no_truncation_control(self):
        self.assertEqual(truncate("abc", 10), "abc")


class TestNormalizeWS(unittest.TestCase):  # T4 target — 1 failing + 1 control
    def test_collapse_and_strip(self):
        self.assertEqual(normalize_ws("  a   b  "), "a b")

    def test_already_clean_control(self):
        self.assertEqual(normalize_ws("a b"), "a b")


class TestWordCount(unittest.TestCase):  # T5 target — stays passing (task = add docstring)
    def test_counts(self):
        self.assertEqual(word_count("one two three"), 3)


class TestTitleCase(unittest.TestCase):  # T6 target — stays passing (task = rename var)
    def test_titlecases(self):
        self.assertEqual(title_case("hello world"), "Hello World")


if __name__ == "__main__":
    unittest.main()
