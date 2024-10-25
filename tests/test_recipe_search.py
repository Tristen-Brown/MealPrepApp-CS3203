import unittest
from RecipeSearch import RecipeSearch

class TestRecipeApp(unittest.TestCase):
    def setUp(self):
        # Initialize the RecipeApp and add some recipes
        self.app = RecipeSearch()
        self.app.add_recipe("Spaghetti Carbonara")
        self.app.add_recipe("Chicken Alfredo")
        self.app.add_recipe("Beef Stroganoff")
    
    def test_search_valid_string(self):
        # Test searching with a valid string that matches a recipe
        result = self.app.search_recipe("Spaghetti")
        self.assertEqual(result, ["Spaghetti Carbonara"])
    
    def test_search_case_insensitive(self):
        # Test searching should be case-insensitive
        result = self.app.search_recipe("chicken")
        self.assertEqual(result, ["Chicken Alfredo"])

    def test_search_partial_match(self):
        # Test searching for a partial match
        result = self.app.search_recipe("Stroganoff")
        self.assertEqual(result, ["Beef Stroganoff"])

    def test_search_invalid_string_empty(self):
        # Test searching with an empty string should raise an error
        with self.assertRaises(ValueError):
            self.app.search_recipe("")

    def test_search_invalid_type(self):
        # Test searching with a non-string input should raise an error
        with self.assertRaises(ValueError):
            self.app.search_recipe(123)

    def test_search_no_match(self):
        # Test searching for a string that doesn't match any recipe
        result = self.app.search_recipe("Pizza")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
