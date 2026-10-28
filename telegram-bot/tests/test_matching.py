import unittest

from bot.config import parse_keywords
from bot.matching import Cooldown, KeywordMatcher

KEYWORDS = parse_keywords(
    '[{"id": "shpargalka", "words": ["шпаргалка", "чек лист"], "url": "https://x"},'
    ' {"id": "guide", "words": ["гайд"], "url": "https://y"}]'
)


class MatcherTest(unittest.TestCase):
    def setUp(self):
        self.matcher = KeywordMatcher(KEYWORDS)

    def test_matches_whole_word_any_case(self):
        for text in ["шпаргалка", "ШПАРГАЛКА!", "Мехоҳам шпаргалка 🔥", "  Шпаргалка."]:
            self.assertEqual(self.matcher.match(text).id, "shpargalka", text)

    def test_phrase_with_extra_spaces(self):
        self.assertEqual(self.matcher.match("Чек   лист лутфан").id, "shpargalka")

    def test_part_of_word_does_not_match(self):
        self.assertIsNone(self.matcher.match("гайдҳо хуб"))
        self.assertIsNone(self.matcher.match("шпаргалкаро"))

    def test_other_keyword(self):
        self.assertEqual(self.matcher.match("гайд").id, "guide")

    def test_empty(self):
        self.assertIsNone(self.matcher.match(None))
        self.assertIsNone(self.matcher.match(""))


class ConfigTest(unittest.TestCase):
    def test_rejects_bad_id(self):
        with self.assertRaises(ValueError):
            parse_keywords('[{"id": "шпаргалка", "words": ["a"], "url": "u"}]')

    def test_rejects_duplicate_id(self):
        with self.assertRaises(ValueError):
            parse_keywords(
                '[{"id": "a", "words": ["x"], "url": "u"}, {"id": "a", "words": ["y"], "url": "u"}]'
            )


class CooldownTest(unittest.TestCase):
    def test_cooldown(self):
        cd = Cooldown(60)
        self.assertTrue(cd.allow(1, "a", now=0))
        self.assertFalse(cd.allow(1, "a", now=30))
        self.assertTrue(cd.allow(2, "a", now=30))
        self.assertTrue(cd.allow(1, "b", now=30))
        self.assertTrue(cd.allow(1, "a", now=61))


if __name__ == "__main__":
    unittest.main()
