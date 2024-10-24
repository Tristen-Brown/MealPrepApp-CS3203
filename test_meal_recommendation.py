import unittest

def is_in_recipe_book(meal_list, recipe_book):
    """Return True if all meals are found in the recipe book."""
    return all(meal in recipe_book for meal in meal_list)

def boundary_check(meal_list):
    """Check the length of the meal list and print appropriate messages."""
    length = len(meal_list)
    if length == 0:
        return "List cannot have zero length"
    elif length > 255:
        return "List cannot be longer than 255"
    else:
        return "List has a valid length"

class TestMealRecommendations(unittest.TestCase):

    def setUp(self):
        """Set up the recipe book for testing."""
        self.recipe_book = ['Chicken', 'Steak', 'Eggs']

    def test_valid_meal_list(self):
        """Test that a valid meal list is identified correctly."""
        valid_list = ['Chicken', 'Steak']
        self.assertTrue(is_in_recipe_book(valid_list, self.recipe_book))

    def test_invalid_meal_list(self):
        """Test that an invalid meal list is flagged correctly."""
        invalid_list = ['Lego', 'Byte']
        self.assertFalse(is_in_recipe_book(invalid_list, self.recipe_book))

    def test_empty_meal_list(self):
        """Test the boundary check for an empty meal list."""
        empty_list = []
        result = boundary_check(empty_list)
        self.assertEqual(result, "List cannot have zero length")

    def test_valid_length_meal_list(self):
        """Test the boundary check for a valid-length meal list."""
        valid_list = ['Chicken', 'Steak']
        result = boundary_check(valid_list)
        self.assertEqual(result, "List has a valid length")

    def test_excessively_long_meal_list(self):
        """Test the boundary check for a meal list longer than 255 items."""
        long_list = [str(i) for i in range(256)]
        result = boundary_check(long_list)
        self.assertEqual(result, "List cannot be longer than 255")

if __name__ == '__main__':
    unittest.main()
