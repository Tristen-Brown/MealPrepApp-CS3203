import time
import unittest

# Main MacrosCalculator class with the four units of functionality.
class MacrosCalculator:
    def __init__(self):
        self.protein = 0
        self.fat = 0
        self.carbs = 0
    
    def input_validation(self, protein, fat, carbs):
        if not isinstance(protein, (int, float)) or not isinstance(fat, (int, float)) or not isinstance(carbs, (int, float)):
            raise ValueError("Inputs must be numeric")
        if protein < 0 or fat < 0 or carbs < 0:
            raise ValueError("Macronutrients must be non-negative")
        return "Valid input"
    
    def macronutrients_calculation(self, protein, fat, carbs):
        target_protein = (100, 200)
        target_fat = (40, 80)
        target_carbs = (150, 300)

        if self.input_validation(protein, fat, carbs) == "Valid input":
            if target_protein[0] <= protein <= target_protein[1] and \
               target_fat[0] <= fat <= target_fat[1] and \
               target_carbs[0] <= carbs <= target_carbs[1]:
                return "Within target range"
            else:
                return "Outside target range"
    
    def clear_calculator(self):
        self.protein, self.fat, self.carbs = 0, 0, 0
    
    def get_macros(self):
        return (self.protein, self.fat, self.carbs)
    
    def load_time(self, protein, fat, carbs):
        start_time = time.time()
        self.macronutrients_calculation(protein, fat, carbs)
        return time.time() - start_time

# Unit tests using unittest framework
class TestMacrosCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = MacrosCalculator()

    # Input Validation Tests
    def test_input_validation_valid(self):
        self.assertEqual(self.calculator.input_validation(50, 20, 30), "Valid input")

    def test_input_validation_invalid_negative(self):
        with self.assertRaises(ValueError):
            self.calculator.input_validation(50, -20, 30)

    # Macronutrients Calculation Tests
    def test_macronutrients_calculation_within_range(self):
        result = self.calculator.macronutrients_calculation(150, 70, 200)
        self.assertEqual(result, "Within target range")

    def test_macronutrients_calculation_outside_range(self):
        result = self.calculator.macronutrients_calculation(50, 20, 50)
        self.assertEqual(result, "Within target range")  # This should fail intentionally

    # Clear Calculator Tests
    def test_clear_calculator(self):
        self.calculator.macronutrients_calculation(100, 40, 120)
        self.calculator.clear_calculator()
        self.assertEqual(self.calculator.get_macros(), (0, 0, 0))

    def test_clear_calculator_failing_case(self):
        self.calculator.macronutrients_calculation(100, 40, 120)
        self.calculator.clear_calculator()
        self.assertEqual(self.calculator.get_macros(), (100, 40, 120))  # This should fail intentionally

    # Load Time Tests
    def test_load_time_within_limit(self):
        start_time = time.time()
        self.calculator.macronutrients_calculation(100, 40, 120)
        load_time = time.time() - start_time
        self.assertLessEqual(load_time, 1)

    def test_load_time_exceeds_limit(self):
        start_time = time.time()
        time.sleep(1.5)
        load_time = time.time() - start_time
        self.assertLessEqual(load_time, 1)  # This should fail intentionally

    # Macronutrient Boundaries Tests
    def test_macronutrient_boundaries_exact_boundary(self):
        result = self.calculator.macronutrients_calculation(150, 60, 250)
        self.assertEqual(result, "Within target range")

    def test_macronutrient_boundaries_above_boundary(self):
        result = self.calculator.macronutrients_calculation(201, 81, 301)
        self.assertEqual(result, "Within target range")  # This should fail intentionally
        
# Run tests if the script is run directly
if __name__ == '__main__':
    unittest.main()
