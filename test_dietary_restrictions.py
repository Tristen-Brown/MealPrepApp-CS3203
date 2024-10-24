MAX_RESTRICTION_LENGTH = 5  # Allow max 5 restrictions

class DietaryRestrictions:
    def __init__(self):
        self.valid_restrictions = ["vegan", "gluten-free", "dairy-free", "keto", "paleo", "nut-free"]

    def validate_restrictions(self, restrictions):
        restriction_list = [r.strip() for r in restrictions.split(",")]

        # Fail Case: Uncomment to trigger failure
        # restriction_list = ["invalid_restriction"]  # Fail Test
        
        # Check that all input restrictions are valid
        for r in restriction_list:
            if r not in self.valid_restrictions:
                return False
        
        # Fail Case: More than 5 restrictions should trigger a failure
        return len(restriction_list) <= MAX_RESTRICTION_LENGTH

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
        # Should Pass: Maximum allowed restrictions
        self.assertTrue(self.dietary_restrictions.validate_restrictions("vegan, gluten-free, dairy-free, keto, paleo"))

    def test_edge_case_empty(self):
        # Should Fail: Empty input
        self.assertFalse(self.dietary_restrictions.validate_restrictions(""))

    def test_edge_case_too_many_restrictions(self):
        # Should Fail: More than 5 restrictions
        self.assertFalse(self.dietary_restrictions.validate_restrictions("vegan, gluten-free, dairy-free, keto, paleo, nut-free"))
# To run the tests
if __name__ == '__main__':
    unittest.main()
