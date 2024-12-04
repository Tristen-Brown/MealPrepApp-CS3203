# Maximum number of dietary restrictions
MAX_RESTRICTION_LENGTH = 10  # Allow max 10 restrictions

class DietaryRestrictions:
    def __init__(self):
        # List of valid dietary restrictions
        self.valid_restrictions = ["vegan", "gluten-free", "dairy-free", "keto", "paleo", "nut-free"]

    def validate_restrictions(self, restrictions):
        # Split and strip input restrictions by commas
        restriction_list = [r.strip() for r in restrictions.split(",")]

        # Check that all input restrictions are valid
        for r in restriction_list:
            if r not in self.valid_restrictions:
                return False
        
        # Check if there are more than the allowed maximum restrictions
        return len(restriction_list) <= MAX_RESTRICTION_LENGTH

# Interactive function to get user input and validate it
def get_user_input_and_validate():
    # Ask user to input dietary restrictions
    restrictions = input("Enter dietary restrictions (comma-separated, e.g. vegan, gluten-free): ")

    # Initialize the DietaryRestrictions class
    dietary_restrictions = DietaryRestrictions()

    # Validate the restrictions
    is_valid = dietary_restrictions.validate_restrictions(restrictions)

    # If invalid, ask for correction or deletion
    while not is_valid:
        print("Test failed! Invalid dietary restrictions or too many restrictions.")
        # Offer user the option to correct or delete input
        action = input("Would you like to delete or correct the input? (Enter 'delete' or 'correct'): ").lower()
        
        if action == 'delete':
            restrictions = input("Please re-enter dietary restrictions (comma-separated, e.g. vegan, gluten-free): ")
        elif action == 'correct':
            restrictions = input("Please correct the dietary restrictions: ")
        else:
            print("Invalid option. Please choose 'delete' or 'correct'.")
            continue
        
        # Revalidate the updated restrictions
        is_valid = dietary_restrictions.validate_restrictions(restrictions)

    # Output the result based on validation
    print("Test passed! Valid dietary restrictions.")

# Unit Tests Class
import unittest

class TestDietaryRestrictions(unittest.TestCase):

    def setUp(self):
        self.dietary_restrictions = DietaryRestrictions()

    def test_valid_restrictions(self):
        # Should Pass: Valid restrictions
        self.assertTrue(self.dietary_restrictions.validate_restrictions("vegan, gluten-free"))

    def test_invalid_restrictions(self):
        # Should Fail: Invalid input
        self.assertFalse(self.dietary_restrictions.validate_restrictions("123, @#%, abcdefg"))

    def test_boundary_case(self):
        # Should Pass: Maximum allowed restrictions (10)
        self.assertTrue(self.dietary_restrictions.validate_restrictions("vegan, gluten-free, dairy-free, keto, paleo, nut-free, vegan, gluten-free, dairy-free, keto"))

    def test_edge_case_empty(self):
        # Should Fail: Empty input
        self.assertFalse(self.dietary_restrictions.validate_restrictions(""))

    def test_edge_case_too_many_restrictions(self):
        # Should Fail: More than 10 restrictions
        self.assertFalse(self.dietary_restrictions.validate_restrictions("vegan, gluten-free, dairy-free, keto, paleo, nut-free, vegan, gluten-free, dairy-free, keto, extra"))

# To run the tests interactively or with unit tests
if __name__ == '__main__':
    # Uncomment the following line if you want to test interactive user input
    get_user_input_and_validate()

    # Uncomment the following line to run the unit tests
    unittest.main()
