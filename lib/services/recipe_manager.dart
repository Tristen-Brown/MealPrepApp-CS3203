class RecipeManager {
  static final RecipeManager _instance = RecipeManager._internal();

  factory RecipeManager() {
    return _instance;
  }

  RecipeManager._internal();

  // Shared list of recipes
  final List<Map<String, String>> recipes = [];

  // Add a recipe
  void addRecipe(String name, String ingredients, String instructions) {
    recipes.add({
      "name": name,
      "ingredients": ingredients,
      "instructions": instructions,
    });
  }

  // Get all recipes
  List<Map<String, String>> getRecipes() {
    return recipes;
  }

  // Delete a recipe
  void deleteRecipe(int index) {
    recipes.removeAt(index);
  }
}
