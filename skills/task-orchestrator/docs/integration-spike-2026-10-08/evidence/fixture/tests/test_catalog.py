import unittest
from catalog import select_names

class CatalogTests(unittest.TestCase):
    def test_default(self):
        names = ["Bee", "ant", "Bee"]
        self.assertEqual(select_names(names), names)
        self.assertEqual(select_names(names, ""), names)
        self.assertEqual(names, ["Bee", "ant", "Bee"])

    def test_selects_case_sensitive_prefix_matches_in_order(self):
        names = ["ant", "Bee", "beetle", "Bee", "Bison", "Beech"]
        self.assertEqual(select_names(names, "Bee"), ["Bee", "Bee", "Beech"])

    def test_returns_empty_for_empty_input_or_no_matches(self):
        self.assertEqual(select_names([], "Bee"), [])
        self.assertEqual(select_names(["ant", "beetle"], "Bee"), [])
