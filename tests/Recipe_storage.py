import unittest

# Recipe Class Definition
class Recipe:
    def __init__(self, name, ingredients, instructions, image=None):
        """Initialize a new recipe with name, ingredients, instructions, and an optional image.
        Args:
            name (str): The name of the recipe.
            ingredients (list): A list of ingredients used in the recipe.
            instructions (str): The step-by-step instructions for preparing the recipe.
            image (str, optional): A URL or file path to an image of the finished recipe. Default is None.
        """
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions
        self.image = image

    def __str__(self):
        """Provide a string representation of the recipe."""
        return f"Recipe: {self.name}"

    def get_details(self):
        """Return a dictionary containing all the recipe details for display."""
        details = {
            "Name": self.name,
            "Ingredients": ', '.join(self.ingredients),
            "Instructions": self.instructions,
            "Image": self.image if self.image else "No image provided"
        }
        return details

# Function to add a new recipe via user input
def add_recipe():
    """Prompts user to input details for a new recipe and adds it to the recipe list."""
    name = input("Enter the recipe name: ")
    ingredients = input("Enter the ingredients, separated by commas: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]  # Clean spaces from user input
    instructions = input("Enter the preparation instructions: ")
    image = input("Enter image URL or path (optional, press enter to skip): ")
    image = image if image.strip() else None  # Only store image if the string is not empty
    recipe = Recipe(name, ingredients, instructions, image)
    recipes.append(recipe)
    print(f"Recipe '{name}' added successfully!\n")

# Function to display all recipes
def view_recipes():
    """Displays all recipes currently stored."""
    if recipes:
        for recipe in recipes:
            print(recipe.get_details())
            print()  # Add a newline for better separation
    else:
        print("No recipes available. Please add some recipes first.\n")

recipes = []  # Global list to store recipes

def main():
    """Main function to run the recipe storage system."""
    while True:
        print("Recipe Storage System")
        print("1. Add a new recipe")
        print("2. View all recipes")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_recipe()
        elif choice == '2':
            view_recipes()
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.\n")

# Unit Testing Class for Recipe
class TestRecipe(unittest.TestCase):
    def setUp(self):
        """Prepare context for each test method."""
        self.ingredients = ["2 eggs", "1/4 cup milk", "1 cup flour"]
        self.instructions = "Mix ingredients and cook on a non-stick pan for 2 minutes each side."
        self.recipe = Recipe("Pancake", self.ingredients, self.instructions)

    def test_recipe_creation(self):
        """Test proper creation and attribute assignment in a recipe."""
        self.assertEqual(self.recipe.name, "Pancake")
        self.assertEqual(self.recipe.ingredients, self.ingredients)
        self.assertEqual(self.recipe.instructions, self.instructions)
        self.assertIsNone(self.recipe.image)  # Image should be None if not provided

    def test_recipe_string_representation(self):
        """Test the string representation of the recipe."""
        self.assertEqual(str(self.recipe), "Recipe: Pancake")

    def test_get_details(self):
        """Test the detail retrieval of a recipe."""
        expected_details = {
            "Name": "Pancake",
            "Ingredients": "2 eggs, 1/4 cup milk, 1 cup flour",
            "Instructions": self.instructions,
            "Image": "No image provided"
        }
        self.assertEqual(self.recipe.get_details(), expected_details)

# Check if the script is run directly and execute accordingly
if __name__ == '__main__':
    main()
    # Uncomment the following line to run tests instead of the main application
    # unittest.main()
