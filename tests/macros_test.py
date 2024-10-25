import unittest
import time
import pytest

# Main MacrosCalculator class with the four units of functionality.
class MacrosCalculator:
    def __init__(self):
        self.protein = 0
        self.fat = 0
        self.carbs = 0
    
    def input_validation(self, protein, fat, carbs):
        # Input Validation: Ensures all inputs are valid numbers and positive.
        if not isinstance(protein, (int, float)) or not isinstance(fat, (int, float)) or not isinstance(carbs, (int, float)):
            raise ValueError("Inputs must be numeric")
        if protein < 0 or fat < 0 or carbs < 0:
            raise ValueError("Macronutrients must be non-negative")
        return "Valid input"
    
    def macronutrients_calculation(self, protein, fat, carbs):
        # Sample fitness goal ranges.
        target_protein = (100, 200)  # Example range in grams
        target_fat = (40, 80)        # Example range in grams
        target_carbs = (150, 300)    # Example range in grams

        if self.input_validation(protein, fat, carbs) == "Valid input":
            if target_protein[0] <= protein <= target_protein[1] and \
               target_fat[0] <= fat <= target_fat[1] and \
               target_carbs[0] <= carbs <= target_carbs[1]:
                return "Within target range"
            else:
                return "Outside target range"
    
    def clear_calculator(self):
        # Clears the macronutrients.
        self.protein, self.fat, self.carbs = 0, 0, 0
    
    def get_macros(self):
        # Returns the current macros (protein, fat, carbs).
        return (self.protein, self.fat, self.carbs)
    
    def load_time(self, protein, fat, carbs):
        # Measures the load time of the calculation.
        start_time = time.time()
        self.macronutrients_calculation(protein, fat, carbs)
        return time.time() - start_time

# Refactored test cases using pytest

# Input Validation Tests
def test_input_validation_valid_input():
    calculator = MacrosCalculator()
    assert calculator.input_validation(50, 20, 30) == "Valid input"

def test_input_validation_invalid_input_non_numeric():
    calculator = MacrosCalculator()
    with pytest.raises(ValueError):
        calculator.input_validation("fifty", 20, 30)

# Failing Test: This should pass valid input but we are forcing it to expect an error (intentional fail)
def test_input_validation_invalid_input_negative_value():
    calculator = MacrosCalculator()
    assert calculator.input_validation(50, -20, 30) == "Valid input"  # This should fail because -20 is invalid


# Macronutrients Calculation Tests
def test_macronutrients_calculation_within_range():
    calculator = MacrosCalculator()
    result = calculator.macronutrients_calculation(150, 70, 200)
    assert result == "Within target range"

# Failing Test: The result is outside the range, but we're testing for 'Within target range' (intentional fail)
def test_macronutrients_calculation_outside_range():
    calculator = MacrosCalculator()
    result = calculator.macronutrients_calculation(50, 20, 50)
    assert result == "Within target range"  # This should fail because it's outside the target range


# Clear Calculator Tests
def test_clear_calculator():
    calculator = MacrosCalculator()
    calculator.macronutrients_calculation(100, 40, 120)
    calculator.clear_calculator()
    assert calculator.get_macros() == (0, 0, 0)

# Failing Test: Expecting the values to not reset, but they do (intentional fail)
def test_clear_calculator_failing_case():
    calculator = MacrosCalculator()
    calculator.macronutrients_calculation(100, 40, 120)
    calculator.clear_calculator()
    assert calculator.get_macros() == (100, 40, 120)  # This will fail because the values should be cleared


# Load Time Tests
def test_load_time_within_limit():
    calculator = MacrosCalculator()
    start_time = time.time()
    calculator.macronutrients_calculation(100, 40, 120)
    load_time = time.time() - start_time
    assert load_time <= 1  # Expect load within 1 second

# Failing Test: Load time is intentionally delayed for failure (intentional fail)
def test_load_time_exceeds_limit():
    start_time = time.time()
    time.sleep(1.5)  # Simulating delay greater than 1 second
    load_time = time.time() - start_time
    assert load_time <= 1  # This will fail because the delay exceeds 1 second


# Macronutrient Boundaries Tests
def test_macronutrient_boundaries_exact_boundary():
    calculator = MacrosCalculator()
    assert calculator.macronutrients_calculation(150, 60, 250) == "Within target range"  # Exact boundary

# Failing Test: Above the boundary (intentional fail)
def test_macronutrient_boundaries_above_boundary():
    calculator = MacrosCalculator()
    assert calculator.macronutrients_calculation(201, 81, 301) == "Within target range"  # This should fail because it's above the boundary


# Run the main function.
if __name__ == "__main__":
    unittest.main()
