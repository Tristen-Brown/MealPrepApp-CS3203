class RecipeSerch:
    def __init__(self):
        self.recipes = []

    def add_recipe(self, recipe_name):
        self.recipes.append(recipe_name)

    def search_recipe(self, query):
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Search query must be a valid non-empty string")
        return [recipe for recipe in self.recipes if query.lower() in recipe.lower()]
