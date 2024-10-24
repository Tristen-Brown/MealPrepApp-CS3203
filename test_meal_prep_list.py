# Maximum meals per day (Ensure only one value is active at a time for testing—either the pass or fail case)
MAX_MEALS_PER_DAY = 3  # This will pass the test
# MAX_MEALS_PER_DAY = 4  # Uncomment this to trigger a test failure

# Meal selection function
def validate_meal_selection(meals_per_day, eating_out=False):
    # If the user selects to eat out, meals_per_day should be 0
    if eating_out:
        return meals_per_day == 0
    
    # Valid meal selection: 2 or 3 meals per day
    return 2 <= meals_per_day <= MAX_MEALS_PER_DAY

# Unit Test Class
import unittest

class TestMealPrepList(unittest.TestCase):
    
    # Test valid meal selection (2 meals)
    def test_valid_meal_selection_2_meals(self):
        self.assertTrue(validate_meal_selection(2))  # Should pass
    
    # Test valid meal selection (3 meals)
    def test_valid_meal_selection_3_meals(self):
        self.assertTrue(validate_meal_selection(3))  # Should pass
    
    # Boundary case: Invalid meal selection (1 meal), should fail
    def test_invalid_meal_selection_1_meal(self):
        self.assertFalse(validate_meal_selection(1))  # Should fail
    
    # Edge case: Eating out, should pass
    def test_eating_out(self):
        self.assertTrue(validate_meal_selection(0, eating_out=True))  # Should pass
    
    # Edge case: More than 3 meals, should fail
    def test_invalid_meal_selection_4_meals(self):
        self.assertFalse(validate_meal_selection(4))  # Should fail

# To run the tests
if __name__ == '__main__':
    unittest.main()
